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
from postleid import presets
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
        guess_1000s: bool = presets.DEFAULT_GUESS_1000S_SHORTENED,
    ) -> None:
        """Find the active sheet in the workbook"""
        self.dataframe = dataframe
        self.guess_1000s = guess_1000s
        self.zip_column = ""
        self.country_column = ""
        for column_name in self.dataframe.columns:
            if not self.zip_column:
                for name_part in presets.ZIP_CODE_HEADING_PARTS:
                    if name_part in column_name.lower():
                        self.zip_column = column_name
                        break
                    #
                #
            #
            if not self.country_column:
                if column_name.lower() in presets.COUNTRY_HEADINGS:
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
        self.dataframe[self.cc_column] = country_source.map(
            self.lookup_country_code
        )
        for line in str(self.dataframe).splitlines():
            commons.LogWrapper.debug(line)
        #
        self.__validator = rule_checks.ValidatorsCache(
            default_cc=presets.DEFAULT_CC
        )

    def lookup_country_code(self, country: Union[float, int, str]) -> str:
        """Lookup the country code for country"""
        country_code = ""
        if isinstance(country, (float, int)):
            return country_code
        #
        try:
            country_code = self.__cc_lookup[country.lower()]
        except KeyError:
            if country:
                commons.LogWrapper.warning(
                    "Country code für {country!r} nicht gefunden"
                )
            #
        #
        if country_code == presets.DEFAULT_CC:
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
            self.dataframe.at[row_number, self.cc_column] or presets.DEFAULT_CC
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
            and self.guess_1000s
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


# vim: fileencoding=utf-8 sw=4 ts=4 sts=4 expandtab autoindent syntax=python:
