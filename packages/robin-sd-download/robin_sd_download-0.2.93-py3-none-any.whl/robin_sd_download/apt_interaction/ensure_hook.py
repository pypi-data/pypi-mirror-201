#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from robin_sd_download.supportive_scripts import logger
from robin_sd_download.supportive_scripts import sudo_file

# script_location = '/opt/robin/scripts/sd/pre_hook.py'


def ensure_hook():
    """Ensures the local apt hook file exists and contains the expected contents."""

    hook_file = "/etc/apt/apt.conf.d/100-robinsw"
    # contents = 'APT::Update::Pre-Invoke  {"/bin/python -m robin_sd_download --pull";};\n'
    contents = 'APT::Update::Pre-Invoke {"python3 -m robin_sd_download --pull";};\n'

 #   contents = contents.replace('script_location', script_location)

    if os.path.isfile(hook_file):
        logger.log(message="Hook file exists, checking contents.",
                   log_level="info", to_terminal=False)
        # Ensure the contents of the file match the contents of the variable
        with open(hook_file, "r") as stream:
            if stream.read() == contents:
                logger.log(message="Hook file contents match",
                           log_level="info", to_terminal=False)
                # logging.info("Hook file contents match")
                return True
            else:
                logger.log(message="Hook file contents do not match, overwriting.",
                           log_level="error", to_terminal=False)
                # Copy the current file to a backup
                sudo_file.rename_sudo_file(
                    old_path=hook_file, new_path=hook_file + ".bak")
                sudo_file.create_sudo_file(
                    full_path=hook_file, contents=contents)
                return True
    else:
        logger.log(message="Hook file does not exist, creating it at " +
                   hook_file, log_level="info", to_terminal=False)
        sudo_file.create_sudo_file(full_path=hook_file, contents=contents)
        return True
