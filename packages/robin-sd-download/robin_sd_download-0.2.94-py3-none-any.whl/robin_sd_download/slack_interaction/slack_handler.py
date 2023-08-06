#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import json
import sys

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from robin_sd_download.supportive_scripts import logger
from robin_sd_download.supportive_scripts import yaml_parser

conversations_store = {}


def zip_files(log_dir):
    try:
        zip_file = shutil.make_archive(log_dir, 'zip', log_dir)
        return zip_file
    except Exception as e:
        logger.log(
            message=f"Error zipping files: {e}", to_terminal=True, log_level='error')


def get_channel_id(slack_client: WebClient, channel_name: str):
    try:
        response = slack_client.conversations_list(limit=1000)
        channels = response['channels']

        for channel in channels:
            if channel['name'] == channel_name:
                return channel['id']

    except SlackApiError as e:
        logger.log(message="Error: " + str(e),
                   to_terminal=True, log_level="error")
        sys.exit(1)


def send_slack(file_to_send: str, customer_name: str = None):
    config = yaml_parser.parse_config()
    slack_token = config['slack']['token']
    slack_channel_name = config['slack']['channel']

    slack_client = WebClient(token=slack_token)

    # Get the channel ID based on the human-readable channel name
    channel_id = get_channel_id(
        channel_name=slack_channel_name, slack_client=slack_client)

    try:
        response = slack_client.files_upload_v2(
            channel=channel_id,
            file=file_to_send,
            title=f"{customer_name}: File upload for SD Downloader" if customer_name else "File upload for SD Downloader",
            filename=os.path.basename(file_to_send),
        )

        if response and response['ok'] or response.status_code == 200:
            logger.log(message="File uploaded successfully.",
                       to_terminal=True, log_level="info")
        else:
            logger.log(message="File upload failed.",
                       to_terminal=True, log_level="error")

    except SlackApiError as e:
        logger.log(message="Error: " + str(e),
                   to_terminal=False, log_level="error")
        logger.log(message="Please find error message in the logfile",
                   to_terminal=True, log_level="info")


def send_slack_entrypoint():
    try:
        config = yaml_parser.parse_config()

        customer_name = config['customer']['name']

        log_dir = config['log']['file']
        log_dir = os.path.dirname(log_dir)

        # Zip the files
        zip_file = zip_files(log_dir)

        # Send the files to Slack
        send_slack(zip_file, customer_name=customer_name)

        # Delete the zip file
        os.remove(zip_file)
    except KeyboardInterrupt:
        logger.log(message="KeyboardInterrupt detected. Stopping the Slack file sending process.",
                   log_level="warning", to_terminal=True)
