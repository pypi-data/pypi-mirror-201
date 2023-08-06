#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import os


def write_file_with_sudo(file_path, contents):
    with open(file_path, 'w') as file:
        file.write(contents)


def run_script_with_sudo(script_path, arguments):
    full_path = os.path.abspath(script_path)
    subprocess.run(['sudo', 'python3', full_path] + arguments, check=True)


def create_sudo_file(full_path, contents):
    # Ensure the full_path string is a string
    file_path = str(full_path)

    # Ensure the contents string is a string
    contents = str(contents)

    # Create a script that will write the file
    write_file_script = '/tmp/write_file_with_sudo.py'

    with open(write_file_script, 'w') as file:
        file.write(f'''
        
def write_file_with_sudo(file_path, contents):
    with open(file_path, 'w') as file:
        file.write(contents)
        
write_file_with_sudo({file_path!r}, {contents!r})
''')

    run_script_with_sudo(write_file_script, [])
    os.remove(write_file_script)


def rename_sudo_file(old_path, new_path):
    # Ensure the full_path string is a string
    old_path = str(old_path)
    new_path = str(new_path)

    # Create a script that will write the file
    rename_file_script = '/tmp/rename_file_with_sudo.py'

    with open(rename_file_script, 'w') as file:
        file.write(f'''

import os
        
def rename_file_with_sudo(old_path, new_path):
    os.rename(old_path, new_path)

rename_file_with_sudo({old_path!r}, {new_path!r})
''')

    run_script_with_sudo(rename_file_script, [])
    os.remove(rename_file_script)
