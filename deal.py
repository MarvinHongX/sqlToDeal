# deal.py
#########################################################################################
# Author  : Hong
# Created : 5/1/2024
# Modified: 5/2/2024
# Notes   :
#########################################################################################
import shutil
import os
import sys
import datetime
import subprocess
from dotenv import load_dotenv


# .env file
load_dotenv()

def get_log_time():
    return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f%z")


def log_message(level, message):
    log_time = get_log_time()
    prefix = {
        'INFO': 'INFO',
        'WARN': 'WARNING',
        'ERROR': 'ERROR'
    }.get(level, 'INFO')

    print(f"{log_time}\t{prefix}\t{message}")
    sys.stdout.flush()


def read_commands_from_file(file_path):
    with open(file_path, 'r') as file:
        commands = file.readlines()
    return commands


def find_first_deal_file(target_dir):
    first_file = None

    deal_files = [file for file in os.listdir(target_dir) if file.endswith('.deal')]
    deal_files.sort(reverse=False)

    if deal_files:
        first_file = os.path.join(target_dir, deal_files[0])

    return first_file


def compare_commp_cid(file_path_1, file_path_2):
    commp_cid_1 = get_commp_cid(file_path_1)
    commp_cid_2 = get_commp_cid(file_path_2)
    
    return commp_cid_1 == commp_cid_2


def get_commp_cid(file_path):
    boostx_command = ["boostx", "commp", file_path]
    boostx_process = subprocess.Popen(boostx_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    boostx_output, _ = boostx_process.communicate()
    boostx_output = boostx_output.decode('utf-8')
    lines = boostx_output.split('\n')

    log_message("INFO", f"boostx command: {boostx_command}")
    log_message("INFO", f"boostx command excuted:\n {boostx_output}")
    
    commp_cid = lines[0].split(':')[1].strip()
    log_message("INFO", f"commp_cid: {commp_cid}")

    return commp_cid


def deal():
    target_dir = os.getenv("TARGET_DIR")
    log_message("INFO", f"Searching for *.deal files in {target_dir}")

    first_deal_file = find_first_deal_file(target_dir)
    if first_deal_file:
        log_message("INFO", f"Found first .deal file: {first_deal_file}")

        # Find corresponding .tar.aes.car file
        tar_aes_car_file = first_deal_file.replace('.deal', '.tar.aes.car')
        if not os.path.exists(tar_aes_car_file):
            log_message("ERROR", f"No corresponding .tar.aes.car file found for {tar_aes_car_file}")
            return

        # Compare CommP CID
        if not compare_commp_cid(tar_aes_car_file, tar_aes_car_file):
            log_message("ERROR", f"Commp CID mismatch: {tar_aes_car_file}")
            
            # Delete
            if os.path.exists(first_deal_file):
                os.remove(first_deal_file)
                log_message("INFO", f"Deleted {first_deal_file}")

            if os.path.exists(tar_aes_car_file):
                os.remove(tar_aes_car_file)
                log_message("INFO", f"Deleted {tar_aes_car_file}")
            
            return

        log_message("INFO", "Commp CID matches.")



        # Execute commands in the .deal file
        commands = read_commands_from_file(first_deal_file)
        for i, command in enumerate(commands, start=1):
            log_message("INFO", f"Command {i}: {command.strip()}")

            try:
                subprocess.run(command.strip(), shell=True, check=True)
                log_message("INFO", f"Command {i} executed successfully.")
            except subprocess.CalledProcessError as e:
                log_message("ERROR", f"Error executing command {i}: {e}")
                return

        os.rename(first_deal_file, first_deal_file.replace('.deal', '.done'))
        log_message("INFO", f"Renamed {first_deal_file} to {first_deal_file.replace('.deal', '.done')}")

    else:
        log_message("WARN", "No .deal files found in the target directory.")
        return



if __name__ == '__main__':
    deal()
