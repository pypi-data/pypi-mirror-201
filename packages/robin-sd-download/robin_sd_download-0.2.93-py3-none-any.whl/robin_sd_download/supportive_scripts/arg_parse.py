#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys

from robin_sd_download.apt_interaction import ensure_hook
from robin_sd_download.apt_interaction import ensure_local_repo
from robin_sd_download.api_interaction import get_software
from robin_sd_download import _version
from robin_sd_download.slack_interaction import slack_handler
from robin_sd_download.supportive_scripts import yaml_parser
from robin_sd_download.supportive_scripts import version_checker
from robin_sd_download.api_interaction import get_software_info
from robin_sd_download.apt_interaction import prepare_install
from robin_sd_download.apt_interaction import offline_install
from robin_sd_download.supportive_scripts import logger


def arg_parser():
    parser = argparse.ArgumentParser(
        description='Robin Radar Systems - Software Puller',
        usage='robin-sd-download [options]',
        prog='Robin Radar Systems Software Puller',
        epilog='To report any bugs or issues, please visit: \
        https://support.robinradar.systems or run: robin-sd-download --slack'
    )

    parser.add_argument('-c', '--check', action='store_true',
                        help='ensure all prerequisites are met')
    parser.add_argument('-p', '--pull', action='store_true',
                        help='pull software from the server')
    parser.add_argument('-i', '--info', action='store_true',
                        help='info about the software version')
    parser.add_argument('-pre', '--prepare', action='store_true',
                        help='prepare the system for offline installation (requires sudo -E)')
    # parser.add_argument('-ins', '--install', action='store_true',
    #                     help='start offline installation (requires sudo -E)')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s {version}'.format(version=_version.__version__))
    parser.add_argument('-s', '--slack', action='store_true',
                        help='Send the logs to IT/DevOps Slack channel')

    args = parser.parse_args()

    config = yaml_parser.parse_config()

    logger.log(message="Starting Robin Radar Systems Software Puller",
               log_level="info", to_terminal=True)
    logger.log(message="Version: " + _version.__version__,
               log_level="info", to_terminal=True)
    logger.log(message="Username: " +
               config['robin_email'], log_level="info", to_terminal=True)

    version_checker.check_latest_version()

    if args.check:
        ensure_hook.ensure_hook()
        ensure_local_repo.ensure_local_repo()
        logger.log(message="All prerequisites met.",
                   log_level="info", to_terminal=True)
        sys.exit(0)

    elif args.pull:
        ensure_hook.ensure_hook()
        ensure_local_repo.ensure_local_repo()
        logger.log(message="Pulling software...",
                   log_level="info", to_terminal=True)
        get_software.get_software()
        sys.exit(0)

    elif args.info:
        get_software_info.get_software_info()
        sys.exit(0)

    elif args.prepare:
        prepare_install.prepare_install()
        sys.exit(0)

    # elif args.install:
    #     offline_install.offline_install()
    #     sys.exit(0)

    elif args.slack:
        slack_handler.send_slack_entrypoint()
        sys.exit(0)

    else:
        parser.print_help()
        sys.exit(1)
