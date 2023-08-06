#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 Bootloader.  All rights reserved.
#
# This software is the confidential and proprietary information of
# Bootloader or one of its subsidiaries.  You shall not disclose this
# confidential information and shall use it only in accordance with the
# terms of the license agreement or other applicable agreement you
# entered into with Bootloader.
#
# BOOTLOADER MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE
# SUITABILITY OF THE SOFTWARE, EITHER EXPRESS OR IMPLIED, INCLUDING BUT
# NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR
# A PARTICULAR PURPOSE, OR NON-INFRINGEMENT.  BOOTLOADER SHALL NOT BE
# LIABLE FOR ANY LOSSES OR DAMAGES SUFFERED BY LICENSEE AS A RESULT OF
# USING, MODIFYING OR DISTRIBUTING THIS SOFTWARE OR ITS DERIVATIVES.

from pathlib import Path
import argparse

from majormode.perseus.constant.logging import LOGGING_LEVEL_LITERAL_STRINGS
from majormode.perseus.constant.logging import LoggingLevelLiteral
from majormode.perseus.utils.logging import DEFAULT_LOGGING_FORMATTER
from majormode.perseus.utils.logging import cast_string_to_logging_level
from majormode.perseus.utils.logging import set_up_logger

from bootloader.ue.utils import uasset_dump


def cast_string_to_path(path: str) -> Path:
    return Path(path)


def parse_arguments() -> argparse.Namespace:
    """
    Convert argument strings to objects and assign them as attributes of
    the namespace.


    @return: An instance `Namespace` corresponding to the populated
        namespace.
    """
    parser = argparse.ArgumentParser(description="Unreal Engine project's asset list dump")

    parser.add_argument(
        '--logging-level',
        dest='logging_level',
        metavar='LEVEL',
        required=False,
        default=str(LoggingLevelLiteral.info),
        type=cast_string_to_logging_level,
        help=f"specify the logging level ({', '.join(LOGGING_LEVEL_LITERAL_STRINGS)})"
    )

    parser.add_argument(
        '--path',
        dest='path',
        metavar='PATH',
        required=True,
        type=cast_string_to_path,
        help="specify the path to root folder of the Unreal Engine project' assets"
    )

    return parser.parse_args()


def run():
    arguments = parse_arguments()

    set_up_logger(logging_formatter=DEFAULT_LOGGING_FORMATTER, logging_level=arguments.logging_level)
    uasset_dump.dump_assets(arguments.path)
