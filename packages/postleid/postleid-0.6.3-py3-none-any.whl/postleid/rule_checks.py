#!/usr/bin/env python

"""

postleid.rule_checks

Formal postal code checks using different rules per country

Copyright (C) 2023 Rainer Schwarzbach

This file is part of postleid.

postleid is free software: you can redistribute it and/or modify
it under the terms of the MIT License.

postleid is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the LICENSE file for more details.

"""


import dataclasses
import math
import re

from typing import Any, Dict, Iterator, List, Optional, Union

# local module
from postleid import commons


class ValidatorError(Exception):

    """Base class for errors raised by this module"""

    def __init__(self, *args: object) -> None:
        """Initialize the base class"""
        super().__init__(*args)
        self.additional_information: List[str] = []

    def add_info(self, *more_info: str) -> None:
        """provide additional information"""
        self.additional_information.extend(more_info)


class InvalidFormatError(ValidatorError):

    """Raised if a candidate does not mantch any defined format"""


class MissingRulesError(ValidatorError):

    """Raised if rules for the provided country are not defined"""


class OutOfRangeError(ValidatorError):

    """Raised if a zip is out of range"""


class UnsupportedDataTypeError(ValidatorError):

    """Raised if a candidate is of an unsupported data type"""


def get_pattern_data(rules: Dict[str, Any]) -> Dict[str, Any]:
    """Return only the rule parts relevant for pattern interpretation"""
    return {
        key: value
        for key, value in rules.items()
        if key
        in ("pattern", "min", "max", "only", "except", "remove_leading_zeroes")
    }


@dataclasses.dataclass
class PartialValueRules:

    """Store rules for partial values"""

    only: List[str]
    excluded: List[str]
    minimum: Optional[int] = None
    maximum: Optional[int] = None
    pattern_length: int = 0
    remove_leading_zeroes: Optional[bool] = False

    def validated_numeric_part(self, numeric_candidate: int) -> str:
        """Return the validated numeric part as string
        or raise an OutOfRangeError on violations
        """
        if self.minimum is not None and numeric_candidate < self.minimum:
            raise OutOfRangeError(
                f"{numeric_candidate} is below defined minimum"
                f" of {self.minimum}"
            )
        #
        if self.maximum is not None and numeric_candidate > self.maximum:
            raise OutOfRangeError(
                f"{numeric_candidate} is above defined maximum"
                f" of {self.maximum}"
            )
        #
        validated_part = f"{numeric_candidate:0{self.pattern_length}d}"
        if self.remove_leading_zeroes:
            validated_part = validated_part.lstrip("0")
        #
        return validated_part

    def check_limitations(self, candidate_part: str) -> None:
        """Check candidate_part against only / except
        and raise an InvalidFormatError on rule violations
        """
        if self.only and candidate_part not in self.only:
            raise InvalidFormatError(
                f"{candidate_part} must be one of {self.only!r}"
            )
        #
        if self.excluded and candidate_part in self.excluded:
            raise InvalidFormatError(
                f"{candidate_part} must not be one of {self.excluded!r}"
            )
        #


class PatternComponent:

    """Check one component"""

    translations = {
        "[a]": "[A-Z]?",
        "[a/n]": r"[A-Z\d]?",
        "a": "[A-Z]",
        "n": r"\d",
        "?": r"[A-Z\d]",
    }
    prx_all_numeric_pattern = re.compile(r"\An+\Z")
    prx_all_numeric_literal = re.compile(r"\A\d+\Z")

    def __init__(self, country_code: str, **rules) -> None:
        """Initialize rules for the country"""
        # rules: literal | pattern, min, max, only, except
        only: List[str] = []
        excluded: List[str] = []
        minimum: Optional[int] = None
        maximum: Optional[int] = None
        remove_leading_zeroes = False
        if "literal" in rules:
            literal = str(rules["literal"])
            only.append(literal)
            self.pattern = literal
            self.__regex = "." * len(literal)
            self.all_numeric = self.prx_all_numeric_literal.match(literal)
        else:
            self.pattern = rules["pattern"]
            if self.pattern == "cc":
                self.__regex = re.escape(country_code.upper())
            else:
                self.__regex = self.__translate_pattern(self.pattern)
                only.extend(str(item) for item in rules.get("only", []))
                excluded.extend(str(item) for item in rules.get("except", []))
                minimum = rules.get("min")
                maximum = rules.get("max")
                remove_leading_zeroes = rules.get(
                    "remove_leading_zeroes", False
                )
            #
            self.all_numeric = self.prx_all_numeric_pattern.match(self.pattern)
            if (
                minimum is not None
                and self.all_numeric
                and remove_leading_zeroes
            ):
                self.__regex = (
                    f"{self.translations['n']}"
                    f"{{{int(math.log10(minimum))},{len(self.pattern)}}}"
                )
            else:
                remove_leading_zeroes = False
            #
        #
        self.__rules = PartialValueRules(
            only,
            excluded,
            minimum=minimum,
            maximum=maximum,
            pattern_length=len(self.pattern),
            remove_leading_zeroes=remove_leading_zeroes,
        )

    @property
    def regex(self) -> str:
        """Return the partial regex"""
        return self.__regex

    @classmethod
    def __translate_pattern(cls, pattern: str) -> str:
        """Translate a pattern to a regular expression"""
        re_parts: List[str] = []
        try:
            re_parts.append(cls.translations[pattern])
        except KeyError:
            for character in pattern:
                re_parts.append(cls.translations[character])
            #
        #
        return "".join(re_parts)

    def validated(self, candidate_part: str) -> str:
        """Validate a postal code part and raise the appropriate Exception
        if it does not conform to the rules.
        Return the validated part.
        """
        validated_part = candidate_part
        try:
            if self.all_numeric:
                validated_part = self.__rules.validated_numeric_part(
                    int(candidate_part, 10)
                )
            #
            self.__rules.check_limitations(validated_part)
        except ValidatorError as error:
            error.add_info(f"Pattern component is {self.pattern!r}")
            raise error
        #
        return validated_part


class VariantChecker:

    """Check one variant"""

    def __init__(self, country_code: str, **rules) -> None:
        """Initialize rules for the country"""
        self.__cc = country_code
        # rules: compound | literal | pattern
        components = rules.get("compound", [])
        self.__components: List[PatternComponent] = []
        if components:
            self.__components.extend(
                PatternComponent(self.__cc, **single_component)
                for single_component in components
            )
        else:
            if "literal" in rules:
                self.__components.append(
                    PatternComponent(self.__cc, literal=rules["literal"])
                )
            elif "pattern" in rules:
                pattern_data = get_pattern_data(rules)
                self.__components.append(
                    PatternComponent(self.__cc, **pattern_data)
                )
            #
        #
        # store the full pattern and regex
        self.__full_pattern = "".join(part.pattern for part in self)
        self.__full_prx = re.compile(
            f"\\A({')('.join(part.regex for part in self)})\\Z"
        )
        self.__all_numeric = all(part.all_numeric for part in self)

    @property
    def full_pattern(self) -> str:
        """Return the full pattern"""
        return self.__full_pattern

    def __getitem__(self, index: int) -> PatternComponent:
        """Return pattern component at index"""
        return self.__components[index]

    def __iter__(self) -> Iterator[PatternComponent]:
        """Return an iterator over the pattern components"""
        return iter(self.__components)

    def __len__(self) -> int:
        """Return the number of pattern components"""
        return len(self.__components)

    def format_post_code(
        self,
        candidate: Union[int, str],
    ) -> str:
        """Return a validated and correctly formatted postal code"""
        # split into components and let the component checkers do the work
        if isinstance(candidate, int):
            if self.__all_numeric:
                candidate = f"{candidate:0{len(self.full_pattern)}d}"
            else:
                raise InvalidFormatError("Not all numeric pattern")
            #
        else:
            candidate = candidate.upper()
        #
        matched = self.__full_prx.match(candidate)
        if not matched:
            raise InvalidFormatError(
                f"{candidate!r} does not match pattern {self.full_pattern!r}"
            )
        #
        validated_parts: List[str] = []
        for c_index, group in enumerate(matched.groups()):
            try:
                validated_parts.append(self[c_index].validated(group))
            except ValidatorError as error:
                error.add_info(
                    f"Candidate {candidate!r} examined part was {group!r}",
                    f"Component #{c_index +1} of {len(self)} in variant",
                )
                raise error
        #
        return "".join(validated_parts)


class CodeChecker:

    """Post code formal check for one country"""

    def __init__(self, country_code: str, **rules) -> None:
        """Initialize rules for the country"""
        self.__cc = country_code
        # rules: comment, urls, variants | literal | pattern | compound
        self.__comment = rules.get("comment", f"{country_code!r} code checker")
        self.__urls = rules.get("urls", [])
        variants = rules.get("variants", [])
        self.__variants: List[VariantChecker] = []
        if variants:
            self.__variants.extend(
                VariantChecker(self.__cc, **single_variant)
                for single_variant in variants
            )
        else:
            if "literal" in rules:
                self.__variants.append(
                    VariantChecker(self.__cc, literal=rules["literal"])
                )
            elif "pattern" in rules:
                pattern_data = get_pattern_data(rules)
                self.__variants.append(
                    VariantChecker(self.__cc, **pattern_data)
                )
            elif "compound" in rules:
                self.__variants.append(
                    VariantChecker(self.__cc, compound=rules["compound"])
                )
            #
        #

    def __iter__(self) -> Iterator[VariantChecker]:
        """Return an iterator over the variants"""
        return iter(self.__variants)

    def format_post_code(
        self,
        candidate: Union[int, str],
    ) -> str:
        """Return a validated and correctly formatted postal code"""
        if not isinstance(candidate, (int, str)):
            raise UnsupportedDataTypeError(
                f"Cannot check {candidate!r},"
                " only integers and strings are supported."
            )
        #
        last_error: ValidatorError = MissingRulesError()
        for v_index, single_variant in enumerate(self):
            try:
                return single_variant.format_post_code(candidate)
            except ValidatorError as error:
                last_error = error
                last_error.add_info(
                    f"Variant #{v_index + 1} of {len(self.__variants)}",
                    f"Full pattern is {single_variant.full_pattern!r}",
                )
            #
        #
        last_error.add_info(
            f"Country: {self.__comment}",
            *[f"<{single_url}>" for single_url in self.__urls],
        )
        raise last_error


class ValidatorsCache:

    """Cache for validators

    load rules for all countries, build and cache rules per country
    lazily on demand.
    """

    def __init__(self, default_cc: str = "us") -> None:
        """Initialize the CodeCheckers cache"""
        self.__rules = commons.load_rules_from_file()
        self.__cache: Dict[str, CodeChecker] = {}
        self.__default_cc = default_cc

    def __getitem__(self, name: str) -> CodeChecker:
        """Return cached country code checker"""
        try:
            return self.__cache[name]
        except KeyError:
            try:
                country_rules = self.__rules[name]
            except KeyError as error:
                raise MissingRulesError from error
            #
            return self.__cache.setdefault(
                name,
                CodeChecker(name, **country_rules),
            )
        #

    def output_validated(
        self,
        candidate: Union[float, int, str],
        country: Optional[str] = None,
    ) -> str:
        """Output a validated post code for the country"""
        if country is None:
            country = self.__default_cc
        #
        if isinstance(candidate, float):
            candidate = int(candidate)
        #
        return self[country].format_post_code(candidate)


# vim: fileencoding=utf-8 sw=4 ts=4 sts=4 expandtab autoindent syntax=python:
