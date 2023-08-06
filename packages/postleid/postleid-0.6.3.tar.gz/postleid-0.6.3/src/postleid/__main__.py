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
import shutil
import sys

from typing import List, Optional

# local imports
from postleid import __version__
from postleid import commons
from postleid import fix_excel_files
from postleid import presets


# Absolute script path
SCRIPT_PATH = pathlib.Path(sys.argv[0]).resolve()


def list_supported_countries() -> int:
    """List supported countries and exit with the matching returncode"""
    try:
        country_names = commons.load_country_names_from_file()
    except OSError as error:
        commons.LogWrapper.error(f"{error}")
        return commons.RETURNCODE_ERROR
    #
    try:
        rules = commons.load_rules_from_file()
    except OSError as error:
        commons.LogWrapper.error(f"{error}")
        return commons.RETURNCODE_ERROR
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
    return commons.RETURNCODE_OK


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
        settings_file=pathlib.Path(presets.DEFAULT_USER_SETTINGS_FILE_NAME),
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
        "-s",
        "--settings-file",
        metavar="EINSTELLUNGSDATEI",
        type=pathlib.Path,
        help="die Datei mit Benutzereinstellungen"
        " (Standardwert: %(default)s im aktuellen Verzeichnis)",
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
    target_path = arguments.output_file
    if target_path:
        target_path = target_path.resolve()
    else:
        target_path = (
            source_path.parent
            / f"{presets.DEFAULT_FIXED_FILE_PREFIX}{source_path.name}"
        )
    #
    if not arguments.settings_file.exists():
        default_settings_path = commons.build_data_file_path(
            "default_user_settings.yaml"
        )
        commons.LogWrapper.info(
            f"Einstellungsdatei {arguments.settings_file}"
            " noch nicht vorhanden",
            f" → erzeuge eine neue aus {default_settings_path} …",
        )
        shutil.copy2(default_settings_path, arguments.settings_file)
        commons.LogWrapper.info("… ok")
    #
    commons.LogWrapper.info(
        f"Lade Einstellungen aus {arguments.settings_file} …"
    )
    loaded_settings = commons.load_yaml_from_path(arguments.settings_file)
    user_settings = commons.UserSettings(**loaded_settings)
    commons.LogWrapper.info("… ok")
    commons.LogWrapper.info(commons.separator_line())
    return fix_excel_files.process_file(
        source_path,
        target_path,
        user_settings=user_settings,
    )


if __name__ == "__main__":
    sys.exit(main())


# vim: fileencoding=utf-8 sw=4 ts=4 sts=4 expandtab autoindent syntax=python:
