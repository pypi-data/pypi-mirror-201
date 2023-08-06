#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pypi_simple import PyPISimple
import sys
# import logging

from robin_sd_download.supportive_scripts import logger
from robin_sd_download.supportive_scripts import yaml_parser
from robin_sd_download import _version


def check_latest_version(package_name: str = "robin-sd-download"):
    """Check if the latest version is installed and document how to update if needed."""
    config = yaml_parser.parse_config()

    current_version = _version.__version__

    pypi = PyPISimple()
    page = pypi.get_project_page(package_name)
    latest_version = page.packages[-1].version

    if current_version == latest_version:
        # logging.info("Latest version detected, proceeding.")
        logger.log(message="Latest version detected, proceeding.",
                   log_level="info", to_terminal=False)
    else:
        logger.log(message="Newer version detected, please update.",
                   log_level="error", to_terminal=True)
        logger.log(message="Current version: " + current_version,
                   log_level="error", to_terminal=True)
        logger.log(message="Latest version: " + latest_version,
                   log_level="error", to_terminal=True)
        logger.log(message="To update, run: pip3 install --upgrade " +
                   package_name, log_level="error", to_terminal=True)
        sys.exit(1)
