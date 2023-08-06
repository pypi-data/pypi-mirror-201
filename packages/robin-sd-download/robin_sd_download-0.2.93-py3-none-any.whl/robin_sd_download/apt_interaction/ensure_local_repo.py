#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from robin_sd_download.supportive_scripts import logger
from robin_sd_download.supportive_scripts import sudo_file
from robin_sd_download.api_interaction import get_software_info


def get_ubuntu_version() -> str:
    """Get the Ubuntu version.

    Returns:
        str: The Ubuntu version or an empty string if an error occurs.
    """
    try:
        ubuntu_version = os.popen("lsb_release -cs").read().strip()
    except (FileNotFoundError, PermissionError) as error:
        logger.log(
            message=f"Error when getting Ubuntu version: {error}", log_level="error", to_terminal=True)
        return False

    return ubuntu_version


def get_actual_version() -> str:
    """Get the actual version of the software.

    Returns:
        str: The actual version of the software.
    """
    software_path = get_software_info.get_software_info()["software_path"]
    filename = os.path.basename(software_path)
    extracted_string = os.path.splitext(filename)[0]
    return extracted_string


def add_public_key(pubkey: str) -> bool:
    """Add the missing public key to the system.

    Args:
        pubkey (str): The public key to be added.

    Returns:
        bool: True if the public key was added successfully, False otherwise.
    """
    try:
        os.system(
            f"sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys {pubkey}")
        logger.log(
            message=f"Added public key: {pubkey}", log_level="info", to_terminal=True)
        return True
    except Exception as error:
        logger.log(
            message=f"Error adding public key: {error}", log_level="error", to_terminal=True)
        return False


def ensure_local_repo() -> bool:
    """Ensures the local apt repository file exists and contains the expected contents.

    Returns:
        bool: True if the local repo file exists and contains the expected contents, or was successfully created.
    """
    repo_file = "/etc/apt/sources.list.d/robin-local.list"

    ubuntu_version = get_ubuntu_version()
    software_version = get_actual_version()

    contents = f"deb file:///opt/robin/download/{software_version}/ {ubuntu_version} main\n"

    if os.path.isfile(repo_file):
        logger.log(
            message=f"Repo file exists, checking contents at {repo_file}", log_level="info", to_terminal=False)
        # Ensure the contents of the file match the contents of the variable
        with open(repo_file, "r") as stream:
            if stream.read() == contents:
                logger.log(message="Repo file contents match",
                           log_level="info", to_terminal=False)
                return True
                # Add the missing public key
                # pubkey = ""
                # if not add_public_key(pubkey):
                #     return False
            else:
                logger.log(message="Repo file contents do not match, overwriting.",
                           log_level="error", to_terminal=True)
                # Copy the current file to a backup
                sudo_file.rename_sudo_file(
                    old_path=repo_file, new_path=f"{repo_file}.bak")
                sudo_file.create_sudo_file(
                    full_path=repo_file, contents=contents)
                return True
                # Add the missing public key
                # pubkey = ""
                # if not add_public_key(pubkey):
                #     return False
    else:
        logger.log(
            message=f"Repo file does not exist, creating it at {repo_file}", log_level="info", to_terminal=False)
        sudo_file.create_sudo_file(full_path=repo_file, contents=contents)

        # Add the missing public key
        # pubkey = ""
        # if not add_public_key(pubkey):
        #     return False

    return True
