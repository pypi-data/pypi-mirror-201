#!/usr/bin/env python

"""

postleid.presets

Presets for postleid

Copyright (C) 2023 Rainer Schwarzbach

This file is part of postleid.

postleid is free software: you can redistribute it and/or modify
it under the terms of the MIT License.

postleid is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the LICENSE file for more details.

"""


# Prefix for the fixed file name
DEFAULT_FIXED_FILE_PREFIX = "fixed-"

# User settings default file name
DEFAULT_USER_SETTINGS_FILE_NAME = "postleid-settings.yaml"

# Logging options
LOG_MESSAGE_FORMAT = "%(levelname)-8s | %(message)s"
LOG_MESSAGE_MAX_WIDTH = 68

#
# Defaults for the commons.UserSettings class
#

# Default country code
DEFAULT_CC = "de"

# Multiply values by 1000 if lower than 1000?
GUESS_1000S = False

# Headings in lower case indicating a country column
COUNTRY_HEADINGS = ("Land", "Staat", "Country")

# Heading parts in lower case indicating a postal code column
POSTAL_CODE_HEADING_PARTS = ("PLZ", "Postleit", "Zip Code")


# vim: fileencoding=utf-8 sw=4 ts=4 sts=4 expandtab autoindent syntax=python:
