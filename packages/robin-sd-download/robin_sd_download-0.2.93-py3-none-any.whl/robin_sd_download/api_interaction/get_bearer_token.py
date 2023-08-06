#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from robin_sd_download.supportive_scripts import logger
from robin_sd_download.supportive_scripts import yaml_parser
from robin_sd_download.api_interaction import get_software_info


def get_bearer_token():

    config = yaml_parser.parse_config()
    
    email_add = config['robin_email']
    password = config['robin_password']
    request_url = config['api_url']

    # Ensure that the api_url is reachable
    if not get_software_info.is_url_accessible(request_url):
        logger.log(message="API URL is not reachable.", log_level="error", to_terminal=True)
        return None

    headers = {
        'Content-Type': 'application/json',
    }

    data = '{"email": "' + email_add + '", "password": "' + password + '"}'
    response = requests.post(request_url + '/api/auth/login', headers=headers, data=data)

    if response.status_code == 200:
        bearer_token = response.json()['token']
        return bearer_token
    else:
        logger.log(message="Failed to get bearer token.", log_level="error", to_terminal=True)
        logger.log(message="Response code: " + str(response.status_code), log_level="error", to_terminal=True)
        logger.log(message="Response text: " + response.text, log_level="error", to_terminal=True)
        logger.log(message="Response headers: " + str(response.headers), log_level="error", to_terminal=False)
        logger.log(message="Data: " + data, log_level="error", to_terminal=False)
        logger.log(message="URL: " + request_url + '/api/auth/login', log_level="error", to_terminal=False)
        logger.log(message="Headers: " + str(headers), log_level="error", to_terminal=False)
        return 1
