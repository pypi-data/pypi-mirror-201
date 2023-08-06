#!/usr/bin/env python

"""

postleid.__main__

Locate and fix postal code information in an excel file
Variant using pandas for excel files handling

Copyright (C) 2023 Rainer Schwarzbach

This file is part of postleid.

postleid is free software: you can redistribute it and/or modify
it under the terms of the MIT License.

postleid is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the LICENSE file for more details.

"""


import argparse
import gettext
import logging
import pathlib
import sys

from typing import List, Optional

import pandas

# local imports
from postleid import __version__
from postleid import commons
from postleid import fix_excel_files
from postleid import presets


# Absolute script path
SCRIPT_PATH = pathlib.Path(sys.argv[0]).resolve()

# Return codes
RETURNCODE_OK = 0
RETURNCODE_ERROR = 1


def list_supported_countries() -> int:
    """List supported countries and exit with the matching returncode"""
    try:
        country_names = commons.load_country_names_from_file()
    except OSError as error:
        commons.LogWrapper.error(f"{error}")
        return RETURNCODE_ERROR
    #
    try:
        rules = commons.load_rules_from_file()
    except OSError as error:
        commons.LogWrapper.error(f"{error}")
        return RETURNCODE_ERROR
    #
    without_rules: List[str] = []
    commons.LogWrapper.info("Supported countries:", commons.separator_line())
    for iso_cc, names in country_names.items():
        line = f"[{iso_cc}] {' / '.join(names)}"
        if iso_cc in rules:
            print(line)
        else:
            without_rules.append(line)
        #
    #
    if without_rules:
        commons.LogWrapper.debug(
            commons.separator_line(),
            "Countries with names but without rules:",
            commons.separator_line(),
            *without_rules,
        )
    #
    without_cleartext = [
        f"[{iso_cc}] {country_rule.get('comment', '')}"
        for iso_cc, country_rule in rules.items()
        if iso_cc not in country_names
    ]
    if without_cleartext:
        commons.LogWrapper.debug(
            commons.separator_line(),
            "Countries with rules but missing cleartext name(s):",
            commons.separator_line(),
            *without_cleartext,
        )
    #
    return RETURNCODE_OK


def _parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command line arguments using argparse
    and return the arguments namespace.

    :param args: a list of command line arguments,
        or None to parse sys.argv
    :returns: the parsed command line arguments as returned
        by argparse.ArgumentParser().parse_args()
    """
    # ------------------------------------------------------------------
    # Argparse translation code adapted from
    # <https://github.com/s-ball/i18nparse>
    translation = gettext.translation(
        "argparse",
        localedir=SCRIPT_PATH.parent / "locale",
        languages=["de"],
        fallback=True,
    )
    argparse._ = translation.gettext  # type: ignore
    argparse.ngettext = translation.ngettext  # type: ignore
    # ------------------------------------------------------------------
    main_parser = argparse.ArgumentParser(
        prog="postleid",
        description="Postleitzahlen in Excel-Dateien korrigieren",
    )
    main_parser.set_defaults(
        loglevel=logging.INFO,
    )
    main_parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Version ausgeben und beenden",
    )
    logging_group = main_parser.add_argument_group(
        "Logging-Optionen",
        "steuern die Meldungsausgaben (Standard-Loglevel: INFO)",
    )
    verbosity = logging_group.add_mutually_exclusive_group()
    verbosity.add_argument(
        "-v",
        "--verbose",
        action="store_const",
        const=logging.DEBUG,
        dest="loglevel",
        help="alle Meldungen ausgeben (Loglevel DEBUG)",
    )
    verbosity.add_argument(
        "-q",
        "--quiet",
        action="store_const",
        const=logging.WARNING,
        dest="loglevel",
        help="nur Warnungen und Fehler ausgeben (Loglevel WARNING)",
    )
    main_parser.add_argument(
        "-g",
        "--guess-1000s",
        action="store_true",
        help="Postleitzahlen unter 1000 mit 1000 multiplizieren"
        " (Achtung, für PLZs aus Bahrain liefert diese Option"
        " falsche Ergebnisse!)",
    )
    main_parser.add_argument(
        "-l",
        "--list-supported-countries",
        action="store_true",
        help="Unterstützte Länder anzeigen"
        " (der Dateiname muss in diesem Fall zwar auch angegeben werden,"
        " wird jedoch ignoriert)",
    )
    main_parser.add_argument(
        "-o",
        "--output-file",
        metavar="AUSGABEDATEI",
        type=pathlib.Path,
        help="die Ausgabedatei (Standardwert: Name der Original-Exceldatei"
        f" mit vorangestelltem {presets.DEFAULT_FIXED_FILE_PREFIX!r})",
    )
    main_parser.add_argument(
        "excel_file",
        metavar="EXCELDATEI",
        type=pathlib.Path,
        help="die Original-Exceldatei",
    )
    return main_parser.parse_args(args)


def main(args: Optional[List[str]] = None) -> int:
    """Check the zip codes in the input file,
    and write fixed results to the output file if necessary.
    """
    arguments = _parse_args(args)
    commons.LogWrapper(arguments.loglevel)
    if arguments.list_supported_countries:
        return list_supported_countries()
    #
    source_path = arguments.excel_file.resolve()
    commons.LogWrapper.info(f"Lade Datei {source_path} …")
    dataframe = pandas.read_excel(source_path)
    data_fixer = fix_excel_files.DataFixer(
        dataframe, guess_1000s=arguments.guess_1000s
    )
    statistics = data_fixer.fix_all_zip_codes()
    everything_is_fine, data_changed = commons.evaluate_results(statistics)
    commons.LogWrapper.info(commons.separator_line())
    if data_changed:
        if everything_is_fine:
            try:
                data_fixer.sort_rows()
            except NotImplementedError:
                commons.LogWrapper.info(
                    "Die Daten werden noch nicht nach Postleitzahlen"
                    " sortiert.",
                    "Das muss in Excel/LibreOffice Calc/… durchgeführt"
                    " werden.",
                )
            #
        else:
            commons.LogWrapper.warning(
                "Da die Orignaldaten nicht fehlerfrei waren,"
                " wurden sie nicht nach Land und Postleitzahl sortiert."
            )
        #
        target_path = arguments.output_file
        if target_path:
            target_path = target_path.resolve()
        else:
            target_path = (
                source_path.parent
                / f"{presets.DEFAULT_FIXED_FILE_PREFIX}{source_path.name}"
            )
        #
        commons.LogWrapper.info(f"Schreibe Ausgabedatei {target_path} …")
        try:
            data_fixer.save(target_path)
        except OSError as error:
            commons.LogWrapper.error(str(error))
            return RETURNCODE_ERROR
        #
    else:
        if everything_is_fine:
            no_errors = "keine Fehler"
        else:
            no_errors = "keine automatisiert behebbaren Fehler"
        #
        commons.LogWrapper.info(
            "Es wird keine Ausgabedatei geschrieben,",
            f"weil die Daten {no_errors} enthalten.",
        )
    #
    return RETURNCODE_OK


if __name__ == "__main__":
    sys.exit(main())


# vim: fileencoding=utf-8 sw=4 ts=4 sts=4 expandtab autoindent syntax=python:
