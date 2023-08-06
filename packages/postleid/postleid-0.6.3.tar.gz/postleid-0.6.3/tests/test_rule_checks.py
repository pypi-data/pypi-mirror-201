# -*- coding: utf-8 -*-

"""

tests.test_rule_checks

Unit test the postleid.rule_checks module

Copyright (C) 2023 Rainer Schwarzbach

This file is part of postleid.

postleid is free software: you can redistribute it and/or modify
it under the terms of the MIT License.

postleid is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the LICENSE file for more details.

"""


from unittest import TestCase

from postleid import rule_checks


InvalidFormat = rule_checks.InvalidFormatError
OutOfRange = rule_checks.OutOfRangeError
MissingRules = rule_checks.MissingRulesError

CORRECT = [
    ("ad", "ad123", "AD123"),
    ("af", 1234, "1234"),
    ("af", "3456", "3456"),
    ("ai", "ai-2640", "AI-2640"),
    ("al", "1001", "1001"),
    ("al", 9799, "9799"),
    ("am", 4299, "4299"),
    ("aq", "biqq 1zz", "BIQQ 1ZZ"),
    ("ar", 2345, "2345"),
    ("ar", "A2345BCD", "A2345BCD"),
    ("as", 96799, "96799"),
    ("as", "96799-1234", "96799-1234"),
    ("at", 9999, "9999"),
    ("au", 200, "0200"),
    ("au", 9999, "9999"),
    ("ax", "ax-22000", "AX-22000"),
    ("az", "AZ 0123", "AZ 0123"),
    ("az", "az 6999", "AZ 6999"),
    ("bb", "bb11000", "BB11000"),
    ("bd", "1000", "1000"),
    ("bd", 9499, "9499"),
    ("bh", 101, "101"),
    ("bh", "101", "101"),
    ("bh", 1216, "1216"),
    ("bm", "ab cd", "AB CD"),
    ("bm", "ab 12", "AB 12"),
]

ERRORS = [
    ("xw", 12345, MissingRules),
    ("ad", "AD099", OutOfRange),
    ("ad", "AD800", OutOfRange),
    ("ad", "123", InvalidFormat),
    ("af", 999, OutOfRange),
    ("af", "4400", OutOfRange),
    ("al", 999, OutOfRange),
    ("al", "9800", OutOfRange),
    ("am", 4300, OutOfRange),
    ("am", 12345, InvalidFormat),
    ("ai", "2640", InvalidFormat),
    ("ai", "AI-2222", InvalidFormat),
    ("aq", "BIQQ 2ZZ", InvalidFormat),
    ("ar", 345, InvalidFormat),
    ("ar", "A0345BCD", OutOfRange),
    ("ar", "I2345BCD", InvalidFormat),
    ("as", 96780, InvalidFormat),
    ("as", "96799-ABCD", InvalidFormat),
    ("at", 999, OutOfRange),
    ("au", 199, OutOfRange),
    ("ax", "AX-77000", InvalidFormat),
    ("az", "AZ 0099", OutOfRange),
    ("az", "AZ 7000", OutOfRange),
    ("bb", 11000, InvalidFormat),
    ("bd", "999", InvalidFormat),
    ("bd", 999, OutOfRange),
    ("bh", "100", OutOfRange),
    ("bh", 1217, OutOfRange),
    ("bm", "ABCD", InvalidFormat),
    ("bm", "AB99", InvalidFormat),
    ("bm", 9999, InvalidFormat),
    ("by", "99999", InvalidFormat),
]


class PostalCodes(TestCase):

    """Test postal codes per country"""

    def test_correct(self):
        """correct codes per country"""
        v_cache = rule_checks.ValidatorsCache()
        for country, candidate, expected_result in CORRECT:
            with self.subTest(country=country, candidate=candidate):
                self.assertEqual(
                    v_cache.output_validated(candidate, country=country),
                    expected_result,
                )
            #
        #

    def test_errors(self):
        """wrong codes per country"""
        v_cache = rule_checks.ValidatorsCache()
        for country, candidate, expected_exception in ERRORS:
            with self.subTest(country=country, candidate=candidate):
                self.assertRaises(
                    expected_exception,
                    v_cache.output_validated,
                    candidate,
                    country=country,
                )
            #
        #


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
