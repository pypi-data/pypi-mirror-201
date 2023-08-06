#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import yaml
import sys
import datetime


def check_file_format(file_path):
    """
    Check if the file is in valid yaml format
    """
    try:
        with open(file_path, 'r') as config_file:
            yaml.safe_load(config_file)
        return True
    except (yaml.parser.ParserError, yaml.scanner.ScannerError) as e:
        print(f"Error: {file_path} is not in valid yaml format. {e}")
        return False


def get_keys(config):
    """
    Returns the keys of a valid yaml file, or None if the file is not found or not in yaml format
    """
    return list(config.keys()) if config else None


def check_and_ask(config):
    """
    Recursively check for undefined keys and ask for input
    """
    if isinstance(config, dict):
        for key in config:
            if config[key] is None:
                config[key] = input(f"Please enter a value for {key}: ")
            elif isinstance(config[key], dict):
                check_and_ask(config[key])


def parse_config():
    config_files = [
        os.path.join(os.path.expanduser(
            "/opt/robin/config/sd-download"), ".sd-download-config.yml"),
        os.path.join(os.path.expanduser(
            "/opt/robin/config/sd-download"), ".sd-download-config.yaml"),
        os.path.join(os.path.expanduser(
            "/opt/robin/config/sd-download"), "sd-download-config.yml"),
        os.path.join(os.path.expanduser(
            "/opt/robin/config/sd-download"), "sd-download-config.yaml"),
        os.path.join(os.path.expanduser("~"), ".sd-download-config.yml"),
        os.path.join(os.path.expanduser("~"), ".sd-download-config.yaml"),
        "sd-download-config.yml",
        "sd-download-config.yaml"
    ]

    config = None
    file = None

    # Set variable config_file to the first config file found
    for cfg_file in config_files:
        if os.path.isfile(cfg_file) and check_file_format(cfg_file):
            with open(cfg_file, 'r') as config_file:
                config = yaml.safe_load(config_file)
                file = cfg_file
                print_used_config_file(cfg_file)

                break
    if not config:
        admin_interface = "https://software-api-admin.robinradar.systems"
        doc_pages = "https://robinradar.atlassian.net/wiki/spaces/DEV/pages/284033095/Software+Deployment+API"
        print(f"Error: no config file found, or its contents are missing. Please check it.")
        print(f"Please browse to {admin_interface} to create a config file.")
        print(
            f"Please browse to {doc_pages} to learn how to create a config file.")
        sys.exit(0)

    check_and_ask(config)

    # write the config file with the new values
    try:
        with open(file, "w") as config_file:
            yaml.dump(config, config_file,
                      allow_unicode=True, width=float("inf"))
    except (OSError, yaml.parser.ParserError, yaml.scanner.ScannerError) as e:
        print(f"Error: Failed to write config file. {e}")

    return config


def print_used_config_file(cfg_file):
    """
    Print the path of the used config file if it has not been printed before
    """
    if print_used_config_file.last_cfg_file != cfg_file:
        cet_tz = datetime.timezone(datetime.timedelta(hours=1), 'CET')
        print(f"{datetime.datetime.now(cet_tz).strftime('%Y-%m-%d %H:%M:%S')} +0100 - INFO - Using config file: {cfg_file}")
        print_used_config_file.last_cfg_file = cfg_file


print_used_config_file.last_cfg_file = None
