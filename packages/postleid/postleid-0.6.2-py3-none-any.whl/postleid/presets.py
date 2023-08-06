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


# Heading parts in lower case indicating a zip code column
ZIP_CODE_HEADING_PARTS = ("plz", "postleit", "zip code")

# Headings in lower case indicating a country column
COUNTRY_HEADINGS = ("land", "staat", "country")

# Prefix for the fixed file name
DEFAULT_FIXED_FILE_PREFIX = "fixed-"

# Append 000 to integer values between 1 and 99?
# (in a future release, this controls whether
#  the --guess-1000s or the --no-guess-1000s flag
#  will be provided as options)
DEFAULT_GUESS_1000S_SHORTENED = False

# Default country code
DEFAULT_CC = "de"

# Logging options
LOG_MESSAGE_FORMAT = "%(levelname)-8s | %(message)s"
LOG_MESSAGE_MAX_WIDTH = 68


# vim: fileencoding=utf-8 sw=4 ts=4 sts=4 expandtab autoindent syntax=python:
