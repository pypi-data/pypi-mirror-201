#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import os
import zipfile
import sys
from robin_sd_download.supportive_scripts import sudo_file
from robin_sd_download.api_interaction import get_software_info
from robin_sd_download.supportive_scripts import logger


def get_local_ip():
    try:
        detected_ip = subprocess.check_output(
            ['hostname', '-I']).decode('utf-8').strip()
    except subprocess.CalledProcessError:
        detected_ip = None

    if detected_ip:
        user_confirmation = input(
            f"Detected local IP address is {detected_ip}. Is this correct? (yes/no): ").strip().lower()
        if user_confirmation == 'yes':
            return detected_ip

    local_ip = input("Please enter the local IP address: ")
    return local_ip


def get_software_details():
    """
    Get the type and version of the software.

    Returns:
        tuple: A tuple containing the software type and version.
    """
    software_info = get_software_info.get_software_info()

    # Extract software type and convert it to lowercase
    software_type = software_info['software_type'].lower()

    # Extract software version
    software_path = software_info["software_path"]
    filename = os.path.basename(software_path)
    software_version = os.path.splitext(filename)[0]

    return software_type, software_version


def check_if_root():
    if os.geteuid() != 0:
        logger.log(message="Please run this script as root: sudo -E robin-sd-download -pre",
                   log_level="error", to_terminal=True)
        sys.exit(1)


def prepare_install():
    """
    Prepare offline apt. This includes:

    - Checking if running as root
    - Checking if enough space is available
    - Getting local IP
    - Getting software type and version
    - Updating sources.list and nvidia.list
    - Creating a zip file
    """

    # Check if running as root
    check_if_root()

    # Get software type and version
    software_type, software_version = get_software_details()

    # Try to find local IP, or prompt user to enter it
    local_ip = get_local_ip()

    # prompt user to enter the ubuntu version of target device
    ubuntu_version = input(
        "Please enter the ubuntu version for the target device (e.g. trusty, xenial, bionic, focal, jammy): ")

    # validate ubuntu_version
    if ubuntu_version not in ['trusty', 'xenial', 'bionic', 'focal', 'jammy']:
        logger.log(message="Invalid ubuntu version. Please try again.",
                   log_level="error", to_terminal=True)
        return

    # Set download folder
    dl_folder = '/var/www/html/download'

    # Checks for the existance of the html files and downloads them if missing (from SD API server?)

    # Check if /var/www/html/download folder exists, and create it if it doesn't
    if not os.path.exists(dl_folder):
        os.makedirs(dl_folder)
        logger.log(message=f"Created {dl_folder} folder.",
                   log_level="info", to_terminal=True)

    # Check if nvidia.list, sources.list, and robin.list files exist in /var/www/html/download folder, and create them if they don't
    file_list = ['nvidia.list', 'sources.list', 'robin.list']
    for file in file_list:
        file_path = os.path.join(dl_folder, file)
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                pass
            logger.log(message=f"Created {file_path} file.",
                       log_level="info", to_terminal=True)

    # Remove zip file if it exists
    zipfile_path = '/var/www/html/download.zip'
    if os.path.isfile(zipfile_path):
        os.remove(zipfile_path)

    # Add Robin package to sources list
    robin_list = f"deb [arch=amd64] http://{local_ip}/robin/{software_type}/{software_version} {ubuntu_version} main"
    logger.log(message=f"Content of robin.list: {robin_list}",
               log_level="info", to_terminal=True)
    sudo_file.write_file_with_sudo(
        os.path.join(dl_folder, 'robin.list'), robin_list)

    # Update sources.list and nvidia.list
    subprocess.run(['sudo', 'sed', '-r', f's/(\b[0-9]{{1,3}}\.){{3}}[0-9]{{1,3}}\b/{local_ip}/', os.path.join(
        dl_folder, 'sources.list'), '-i'], check=True)
    subprocess.run(['sudo', 'sed', '-r', f's/(\b[0-9]{{1,3}}\.){{3}}[0-9]{{1,3}}\b/{local_ip}/', os.path.join(
        dl_folder, 'nvidia.list'), '-i'], check=True)

    # Create zip file
    with zipfile.ZipFile(zipfile_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(dl_folder):
            for file in files:
                zipf.write(os.path.join(root, file), file)

    logger.log(message=f"Zip file created successfully at {zipfile_path}",
               log_level="info", to_terminal=True)
