#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import os
import zipfile
import datetime
import glob

from robin_sd_download.api_interaction import get_bearer_token
from robin_sd_download.supportive_scripts import yaml_parser
from robin_sd_download.supportive_scripts import logger

import itertools
from contextlib import closing


def generate_response_content(response, chunk_size=8192):
    try:
        for chunk in response.iter_content(chunk_size=chunk_size):
            if chunk:
                yield chunk
    except KeyboardInterrupt:
        response.close()
        raise


def create_backup_if_exists(folder_path):
    if os.path.exists(folder_path):
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        backup_folder = os.path.join(os.path.dirname(folder_path), "backup")
        os.makedirs(backup_folder, exist_ok=True)

        backup_file_name = f"{os.path.basename(folder_path)}_backup_{timestamp}.zip"
        backup_file_path = os.path.join(backup_folder, backup_file_name)

        with zipfile.ZipFile(backup_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(
                        file_path, folder_path))

        logger.log(
            message=f"Created a backup: {backup_file_path}", log_level="info", to_terminal=True)

        # Keep only the last 3 backup files
        backup_files = glob.glob(os.path.join(
            backup_folder, f"{os.path.basename(folder_path)}_backup_*.zip"))
        backup_files.sort(key=os.path.getctime, reverse=True)

        while len(backup_files) > 3:
            oldest_file = backup_files.pop()
            os.remove(oldest_file)
            logger.log(
                message=f"Removed old backup: {oldest_file}", log_level="info", to_terminal=True)


def get_software():
    config = yaml_parser.parse_config()

    radar_id = config['radar_id']
    request_url = config['api_url']

    # current_date = datetime.datetime.now().strftime("%d%m%Y%H%M%S")

    try:
        bearer_token = str(get_bearer_token.get_bearer_token())
    except KeyboardInterrupt:
        logger.log(
            message="Aborted by user.", log_level="error", to_terminal=True)
        return 1
    except Exception as e:

        logger.log(
            message=f"Failed to get bearer token: {str(e)}", log_level="error", to_terminal=True)
        return 1

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + bearer_token,
    }

    api_endpoint = '/api/radars/' + radar_id + '/software'

    try:
        response = requests.get(
            request_url + api_endpoint, allow_redirects=True, headers=headers, stream=True)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logger.log(
            message=f"Failed to get software: {str(e)}", log_level="error", to_terminal=True)
        return 1

    # Get the name of the file
    file_name = response.headers.get("Content-Disposition").split("=")[1]
    file_name = file_name.replace('"', '')
    file_name = file_name.replace('.zip', '')

    # Define the location to save the file
    file_location = config['static']['download_location']

    try:
        # Create the destination folder
        os.makedirs(file_location, exist_ok=True)

        # Write the file to disk
        write_file = os.path.join(
            file_location, f"{file_name}.zip")

        with open(write_file, 'wb') as f:
            try:
                for chunk in generate_response_content(response, chunk_size=8192):
                    f.write(chunk)
            except KeyboardInterrupt:
                logger.log(
                    message="Download interrupted by user, cleaning up...",
                    log_level="warning", to_terminal=True)
                f.close()
                os.remove(write_file)
                return 1

        logger.log(message="Downloaded to " + write_file,
                   log_level="info", to_terminal=True)

        # Extract the file
        try:
            extracted_folder_path = os.path.join(file_location, f"{file_name}")
            create_backup_if_exists(extracted_folder_path)

            with zipfile.ZipFile(write_file, "r") as zip_ref:
                zip_ref.extractall(extracted_folder_path)
        except zipfile.BadZipFile:
            logger.log(message="The downloaded file is not a valid zip file",
                       log_level="error", to_terminal=True)
            return 1

        # Remove the zip file
        os.remove(write_file)

    except Exception as e:
        logger.log(
            message=f"Failed to download software: {str(e)}", log_level="error", to_terminal=True)
        return 1

    return 0
