#!/usr/bin/env python

"""

postleid.fix_excel_files

Class for fixing postal codes in excel files

Copyright (C) 2023 Rainer Schwarzbach

This file is part of postleid.

postleid is free software: you can redistribute it and/or modify
it under the terms of the MIT License.

postleid is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the LICENSE file for more details.

"""


import pathlib

from typing import Any, Dict, List, Union

import numpy
import pandas

# local imports
from postleid import commons
from postleid import rule_checks


class DataFixer:

    """Fix cells in a workbook"""

    cc_column = "country_code"

    results_by_error = {
        rule_checks.InvalidFormatError: commons.S_WRONG_FORMAT,
        rule_checks.MissingRulesError: commons.S_MISSING_RULES,
        rule_checks.OutOfRangeError: commons.S_OUT_OF_RANGE,
        rule_checks.UnsupportedDataTypeError: commons.S_WRONG_DATA_TYPE,
    }

    def __init__(
        self,
        dataframe: pandas.DataFrame,
        user_settings: commons.UserSettings,
    ) -> None:
        """Find the active sheet in the workbook"""
        self.dataframe = dataframe
        self.user_settings = user_settings
        self.zip_column = ""
        self.country_column = ""
        postal_code_heading_parts = [
            part.lower()
            for part in self.user_settings.postal_code_heading_parts
        ]
        country_headings = [
            heading.lower() for heading in self.user_settings.country_headings
        ]
        for column_name in self.dataframe.columns:
            preprocessed_name = column_name.strip().lower()
            if not self.zip_column:
                for name_part in postal_code_heading_parts:
                    if name_part in preprocessed_name:
                        self.zip_column = column_name
                        break
                    #
                #
            #
            if not self.country_column:
                if preprocessed_name in country_headings:
                    self.country_column = column_name
                #
            #
            if column_name == self.cc_column:
                self.cc_column = f"{column_name}_x"
            #
        #
        # Build a cc column
        self.__cc_lookup: Dict[str, str] = {}
        for (
            iso_cc,
            country_names,
        ) in commons.load_country_names_from_file().items():
            for name in country_names:
                self.__cc_lookup[name.lower()] = iso_cc
            #
        #

        if self.country_column:
            commons.LogWrapper.debug(
                f"Reading country data from {self.country_column}"
            )
            country_source = self.dataframe[self.country_column]
        else:
            country_source = pandas.Series(self.dataframe.index)
        #
        # Map ISO-3166-1 ALPHA-2 codes to country names
        # using the self.lookup_country_code() function because
        # a simple dict is not sufficient (that would produce
        # NaN values for unmatched country names), and we need
        # even more flexibility than a collections.defaultdict()
        # could provide.
        self.dataframe[self.cc_column] = country_source.map(
            self.lookup_country_code
        )
        for line in str(self.dataframe).splitlines():
            commons.LogWrapper.debug(line)
        #
        self.__validator = rule_checks.ValidatorsCache(
            default_cc=self.user_settings.default_country_code
        )

    def lookup_country_code(self, country: Union[float, int, str]) -> str:
        """Lookup the country code for the given country"""
        country_code = ""
        if isinstance(country, (float, int)):
            return country_code
        #
        preprocessed_name = country.strip().lower()
        try:
            country_code = self.__cc_lookup[preprocessed_name]
        except KeyError:
            if preprocessed_name:
                country_code = "??"
                commons.LogWrapper.warning(
                    f"Country code für {country!r} nicht gefunden,"
                    f" verwende {country_code!r}."
                )
            #
        #
        if country_code == self.user_settings.default_country_code:
            return ""
        #
        return country_code

    def fix_all_zip_codes(self) -> List[str]:
        """Fix all zip codes in an Excel workbook.
        Returns statistics (a list of keywords).
        """
        statistics: List[str] = []
        for row_number in self.dataframe.index:
            statistics.append(self.fix_single_cell(row_number))
        #
        return statistics

    def fix_single_cell(self, row_number: int) -> str:
        """Fix the zip code in a single cell.
        Delegate fixing to the appropriate operation
        for the cell content type and log the message.
        Return the operation result.
        """
        original_value = self.dataframe.at[row_number, self.zip_column]
        preprocessed_value = self.__preprocess_cell_value(original_value)
        country_code = (
            self.dataframe.at[row_number, self.cc_column]
            or self.user_settings.default_country_code
        )
        error_details: List[str] = []
        result = commons.S_MISSING_RULES
        try:
            new_value = self.__validator.output_validated(
                preprocessed_value, country=country_code
            )
        except rule_checks.ValidatorError as error:
            error_details.extend(error.args)
            error_details.extend(error.additional_information)
            result = self.results_by_error[type(error)]
        #
        if error_details:
            commons.LogWrapper.warning(
                f"{row_number:>5}  →  Originalwert: {original_value!r}",
                f"      {result} - {error_details[0]}",
            )
            commons.LogWrapper.debug(
                *[f"          - {detail}" for detail in error_details[1:]],
                "      --- Typ nach Vorbehandlung:"
                f" {type(preprocessed_value)}",
            )
            return result
        #
        if new_value == original_value:
            result, details = commons.S_UNCHANGED, "keine Anpassung nötig"
        else:
            self.dataframe.at[row_number, self.zip_column] = new_value
            result, details = commons.S_FIXED, f"neuer Wert: {new_value!r}"
        #
        commons.LogWrapper.debug(
            f"{row_number:>5}  →  Originalwert: {original_value!r}",
            f"      {result} – {details}",
        )
        return result

    def __preprocess_cell_value(
        self, original_value: Any
    ) -> Union[float, int, str]:
        """Return a preprocessed variant of the original value"""
        preprocessed_value = original_value
        if isinstance(original_value, str):
            try:
                preprocessed_value = float(original_value.replace(",", "."))
            except ValueError:
                pass
            else:
                commons.LogWrapper.debug(
                    f"       --- {original_value}"
                    f" → Float: {preprocessed_value}"
                )
            #
        #
        if isinstance(preprocessed_value, numpy.integer):
            preprocessed_value = int(preprocessed_value)
        elif isinstance(preprocessed_value, numpy.inexact):
            preprocessed_value = float(preprocessed_value)
        #
        if (
            isinstance(preprocessed_value, (int, float))
            and self.user_settings.guess_1000s
            and preprocessed_value < 1000
        ):
            return preprocessed_value * 1000
        #
        return preprocessed_value

    def sort_rows(self):
        """Sort table rows by country code and zip"""
        commons.LogWrapper.info(
            "Sortiere Daten nach Land und Postleitzahl ..."
        )
        self.dataframe = self.dataframe.sort_values(
            [self.cc_column, self.zip_column]
        )

    def save(self, output_file: pathlib.Path) -> None:
        """Save the dataframe"""
        del self.dataframe[self.cc_column]
        self.dataframe.to_excel(output_file, index=False)


def process_file(
    source_path: pathlib.Path,
    target_path: pathlib.Path,
    user_settings: commons.UserSettings = commons.UserSettings(),
) -> int:
    """Process the file provided in source_path,
    write output to target_path
    and return the appropriate return code
    """
    commons.LogWrapper.info(f"Lade Datei {source_path} …")
    dataframe = pandas.read_excel(source_path)
    commons.LogWrapper.info("… ok")
    data_fixer = DataFixer(dataframe, user_settings)
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
        commons.LogWrapper.info(f"Schreibe Ausgabedatei {target_path} …")
        try:
            data_fixer.save(target_path)
        except OSError as error:
            commons.LogWrapper.error(str(error))
            return commons.RETURNCODE_ERROR
        #
        commons.LogWrapper.info("… ok")
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
    return commons.RETURNCODE_OK


# vim: fileencoding=utf-8 sw=4 ts=4 sts=4 expandtab autoindent syntax=python:
