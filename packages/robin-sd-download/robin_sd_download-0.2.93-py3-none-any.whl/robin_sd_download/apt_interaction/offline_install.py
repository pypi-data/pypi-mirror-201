# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import subprocess
import os
import getpass
import math
import shutil

from robin_sd_download.supportive_scripts import logger

REQUIRED_SPACE_GB = 30  # Minimum required space on the disk in GB

# (it needs to be moved, when downloading the robin_sd_download package -> sudo apt-get install sshpass)


def check_if_root():
    if os.geteuid() != 0:
        logger.log(message="Please run this script as root: sudo -E robin-sd-download -ins",
                   log_level="error", to_terminal=True)
        sys.exit(1)


def bytes_to_gigabytes(value: int) -> float:
    return value / math.pow(1024, 3)


def gigabytes_to_bytes(value: float) -> int:
    return int(value * math.pow(1024, 3))


def check_space():
    """
    Check if required amount of space is available on the disk.
    """
    total, used, available_space = shutil.disk_usage('/')
    required_space = gigabytes_to_bytes(REQUIRED_SPACE_GB)
    if available_space < required_space:
        logger.log(message=f"Not enough space on the disk. Available space: {bytes_to_gigabytes(available_space):.2f} GB, Required space: {bytes_to_gigabytes(required_space):.2f} GB",
                   log_level="error", to_terminal=True)
        return False
    return True


def install_sshpass():
    try:
        subprocess.run(["sshpass", "-V"], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("sshpass is already installed.")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("sshpass not found. Attempting to install...")
        try:
            if sys.platform.startswith("linux"):
                subprocess.run(["sudo", "apt-get", "update"], check=True)
                subprocess.run(["sudo", "apt-get", "install",
                               "-y", "sshpass"], check=True)
                print("sshpass installed successfully.")
            else:
                print(
                    "Unsupported platform for sshpass installation. Please install sshpass manually.")
                raise Exception(
                    "Unable to install sshpass. Terminating script.")
        except subprocess.CalledProcessError as e:
            print(f"Error during sshpass installation: {e}")
            raise Exception("Unable to install sshpass. Terminating script.")

# remote machine does not have internet => can not install unzip
# therefore install unzip on local machine (like sshpass) then copy it to remote machine


def install_unzip(remote_username, remote_pass, remote_ip):
    try:
        check_unzip_cmd = f"sshpass -p {remote_pass} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null {remote_username}@{remote_ip} 'unzip -v'"
        subprocess.run(check_unzip_cmd, shell=True, check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("unzip is already installed on the remote machine.")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("unzip not found on the remote machine. Attempting to install...")
        try:
            install_unzip_cmd = f"sshpass -p {remote_pass} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null {remote_username}@{remote_ip} 'sudo apt-get update && sudo apt-get install -y unzip'"
            subprocess.run(install_unzip_cmd, shell=True, check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("unzip installed successfully on the remote machine.")
        except subprocess.CalledProcessError as e:
            print(f"Error during unzip installation on remote machine: {e}")
            raise Exception(
                "Unable to install unzip on remote machine. Terminating script.")


def get_remote_ip():
    try:
        detected_ip = subprocess.check_output(
            ['hostname', '-I']).decode('utf-8').strip()
    except subprocess.CalledProcessError:
        detected_ip = None

    if detected_ip:
        user_confirmation = input(
            f"Detected target IP address is {detected_ip}. Is this correct? (yes/no): ").strip().lower()
        if user_confirmation == 'yes':
            return detected_ip

    remote_ip = input("Please enter the IP address of the target device: ")
    return remote_ip


def check_web_servers():
    """
    Check if Nginx or Apache is running on the device.
    """
    nginx_process = subprocess.run(
        ["pgrep", "nginx"], capture_output=True, text=True)
    apache_process = subprocess.run(
        ["pgrep", "apache2"], capture_output=True, text=True)

    if nginx_process.returncode == 0:
        logger.log(message="Nginx is running on this device.",
                   log_level="info", to_terminal=True)
    elif apache_process.returncode == 0:
        logger.log(message="Apache is running on this device.",
                   log_level="info", to_terminal=True)
    else:
        logger.log(message="Neither Nginx nor Apache is running on this device.",
                   log_level="error", to_terminal=True)


def create_temp_folder_on_remote(remote_username, remote_pass, remote_ip, dl_folder):
    create_temp_folder_cmd = f"sshpass -p {remote_pass} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null {remote_username}@{remote_ip} 'sudo mkdir -p {dl_folder}'"
    subprocess.run(create_temp_folder_cmd, shell=True, check=True)

    change_owner_cmd = f"sshpass -p {remote_pass} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null {remote_username}@{remote_ip} 'sudo chown -R {remote_username}: {dl_folder}'"
    subprocess.run(change_owner_cmd, shell=True, check=True)

    logger.log(message=f"Created {dl_folder} folder on remote machine.",
               log_level="info", to_terminal=True)


def copy_files_to_remote(zipfile_path, remote_username, remote_pass, remote_ip):
    if not os.path.exists(zipfile_path):
        logger.log(f"Zip file '{zipfile_path}' not found. Exiting.",
                   log_level="error", to_terminal=True)
        sys.exit(1)

    remote_destination = f'{remote_username}@{remote_ip}:/home/robin/temp'
    logger.log(f"Copying files to {remote_destination}",
               log_level="info", to_terminal=True)
    subprocess.run(['sshpass', '-p', remote_pass, 'scp', '-o', 'StrictHostKeyChecking=no', '-o',
                    'UserKnownHostsFile=/dev/null', zipfile_path, remote_destination], check=True)
    logger.log(f"Files copied to {remote_destination}",
               log_level="info", to_terminal=True)

    sudo_chown_cmd = f"sshpass -p {remote_pass} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null {remote_username}@{remote_ip} 'sudo chown -R {remote_username}: /home/robin/temp'"
    logger.log(
        f"Changing ownership of {remote_destination} to {remote_username}", log_level="info", to_terminal=True)
    subprocess.run(sudo_chown_cmd, shell=True, check=True)
    logger.log(
        f"Ownership changed for {remote_destination}", log_level="info", to_terminal=True)


def unzip_files_on_remote(remote_username, remote_pass, remote_ip, zipfile_path, dl_folder):
    unzip_cmd = f"sshpass -p {remote_pass} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null {remote_username}@{remote_ip} 'unzip {zipfile_path} -d {dl_folder}'"
    try:
        subprocess.run(unzip_cmd, shell=True, check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        logger.log(message="Unzipped files successfully on remote machine.",
                   log_level="info", to_terminal=True)
    except subprocess.CalledProcessError as e:
        logger.log(
            message=f"Error during unzip on remote machine: {e}", log_level="error", to_terminal=True)
        return False


def create_backup_folder_on_remote(remote_username, remote_pass, remote_ip, backup_folder):
    create_backup_folder_cmd = f"sshpass -p {remote_pass} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null {remote_username}@{remote_ip} 'now=`date \"+%Y-%m-%d\"`; mkdir -p {backup_folder}/$now'"
    subprocess.run(create_backup_folder_cmd, shell=True, check=True)
    backup_dir_name = subprocess.check_output(
        f"sshpass -p {remote_pass} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null {remote_username}@{remote_ip} 'basename $(ls -td {backup_folder}/*/ | head -1)'", shell=True).strip().decode("utf-8")
    logger.log(message=f"Created {backup_folder}/{backup_dir_name} folder on remote machine.",
               log_level="info", to_terminal=True)
    return backup_dir_name


def backup_apt_sources_on_remote(remote_username, remote_pass, remote_ip, backup_dir):
    backup_sources_cmd = f"sudo cp /etc/apt/sources.list {backup_dir} && sudo cp /etc/apt/sources.list.d/* {backup_dir} && sudo /usr/local/robin/backup/createBackup"
    ssh_cmd = f"sshpass -p {remote_pass} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null {remote_username}@{remote_ip}"
    subprocess.run(f"{ssh_cmd} '{backup_sources_cmd}'", shell=True, check=True)
    logger.log(message="Successfully backed up apt sources and keys on remote machine.",
               log_level="info", to_terminal=True)


def move_apt_sources_on_remote(remote_username, remote_pass, remote_ip, temp_folder):
    move_sources_cmd = f"sudo mv {temp_folder}/sources.list /etc/apt/sources.list && sudo mv {temp_folder}/nvidia.list /etc/apt/sources.list.d/ && sudo mv {temp_folder}/robin.list /etc/apt/sources.list.d/"
    ssh_cmd = f"sshpass -p {remote_pass} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null {remote_username}@{remote_ip}"
    subprocess.run(f"{ssh_cmd} '{move_sources_cmd}'", shell=True, check=True)
    logger.log(message="Successfully moved apt sources to remote machine.",
               log_level="info", to_terminal=True)


def add_apt_keys_on_remote(remote_username, remote_pass, remote_ip, temp_folder):
    add_keys_cmd = f"sudo apt-key add {temp_folder}/cuda.pub && sudo apt-key add {temp_folder}/robin.pub"
    ssh_cmd = f"sshpass -p {remote_pass} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null {remote_username}@{remote_ip}"
    subprocess.run(f"{ssh_cmd} '{add_keys_cmd}'", shell=True, check=True)
    logger.log(message="Successfully added apt keys to remote machine.",
               log_level="info", to_terminal=True)


def run_update_on_remote(remote_username, remote_pass, remote_ip, temp_folder):
    ps3_prompt = "Should We Run an Update?: "
    options = ["Y", "N", "Q"]
    update_choice = None
    while update_choice is None:
        try:
            update_choice = int(input(f"{ps3_prompt} {options} "))
            if update_choice < 0 or update_choice > len(options) - 1:
                print("Invalid option. Please try again.")
                update_choice = None
        except ValueError:
            print("Invalid input. Please enter a number.")
            update_choice = None
    if update_choice == 0:
        update_cmd = f"sudo apt purge robin-* && sudo apt update -y && sudo apt dist-upgrade -y && sudo apt install cuda-runtime-10-0 && sudo apt install {temp_folder}/*.deb && sudo apt install robin-*"
        ssh_cmd = f"sshpass -p {remote_pass} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null {remote_username}@{remote_ip}"
        subprocess.run(f"{ssh_cmd} '{update_cmd}'", shell=True, check=True)
        logger.log(message="Successfully updated remote machine.",
                   log_level="info", to_terminal=True)
    elif update_choice == 1:
        logger.log(message="Script will not run updates on remote machine.",
                   log_level="info", to_terminal=True)
    else:
        logger.log(message="Aborting update command.",
                   log_level="info", to_terminal=True)


def run_cleanup_on_remote(remote_username, remote_pass, remote_ip):
    cleanup_cmd = "cd /home/robin && sudo rm -rf temp && sudo rm remote_install.sh && sudo rm -rf download*"
    ssh_cmd = f"sshpass -p {remote_pass} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null {remote_username}@{remote_ip}"
    subprocess.run(f"{ssh_cmd} '{cleanup_cmd}'", shell=True, check=True)
    logger.log(message="Successfully cleaned up remote machine.",
               log_level="info", to_terminal=True)


def offline_install():
    """Prepare install function is needed to be run before this function. This function will install the software on the remote machine.

    Returns:
        bool: True if the software was successfully installed, False otherwise.
    """
    # Check if running as root
    check_if_root()

    # Check if required amount of space is available in a partition with at least 1 TB of free space
    if not check_space():
        return

    # Check if Nginx or Apache is running on this device
    check_web_servers()

    # Try to find remote IP of target device, or prompt user to enter it
    remote_ip = get_remote_ip()

    # Prompt user to enter username for remote device
    remote_username = input(
        "Please enter the username for the target device: ")

    # prompt user to enter pass for remote device
    remote_pass = getpass.getpass(
        "Please enter the password for the target device: ")

    # Check if sshpass is installed (it needs to be moved, when downloading the robin_sd_download package -> sudo apt-get install sshpass)
    install_sshpass()

    # Check if unzip is installed on REMOTE (it needs to be moved, when downloading the robin_sd_download package -> sudo apt-get install unzip)
    install_unzip(remote_username, remote_pass, remote_ip)

    # Create /home/robin/temp/ folder for unzipped files on remote device
    create_temp_folder_on_remote(
        remote_username, remote_pass, remote_ip, '/home/robin/temp/')

    # Copy /var/www/html/download.zip folder from local to remote system (into /home/robin/temp/)
    copy_files_to_remote('/var/www/html/download.zip', remote_username,
                         remote_pass, remote_ip)

    # Unzip the files in the temp folder on remote device
    unzip_files_on_remote(remote_username, remote_pass,
                          remote_ip, '/home/robin/temp/download.zip', '/home/robin/temp/')

    # Create backup folder at /home/robin/backup on remote device
    backup_dir = create_backup_folder_on_remote(
        remote_username, remote_pass, remote_ip, '/home/robin/backup/')

    # Backup apt sources and keys on remote device
    backup_apt_sources_on_remote(
        remote_username, remote_pass, remote_ip, backup_dir)

    # Move apt sources and keys from /home/robin/temp/download to /etc/apt/sources.list and /etc/apt/sources.list.d/ on remote device
    move_apt_sources_on_remote(remote_username, remote_pass,
                               remote_ip, '/home/robin/temp/download')

    # Add apt-keys in temp folder (cuda, robin.pub) to remote device
    add_apt_keys_on_remote(remote_username, remote_pass,
                           remote_ip, '/home/robin/temp/download')

    # Run update on remote device
    run_update_on_remote(remote_username, remote_pass,
                         remote_ip, '/home/robin/temp/download')

    # Running Cleanup on remote device
    run_cleanup_on_remote(remote_username, remote_pass, remote_ip)
