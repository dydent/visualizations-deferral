import os
import json
from typing import List


# ---------------------------------------------------------------------------------
# helper functions to load evaluation data from json evaluation log files
# ---------------------------------------------------------------------------------


def load_json_data(file_path: str) -> list:
    """ function to load a pandas df from a .json data file """
    with open(file_path, "r") as file:
        data: list = json.load(file)

    return data


def get_all_json_files(directory: str) -> List[str]:
    """ get all json files from a directory and return a list"""
    json_files = []

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                json_files.append(os.path.join(root, file))

    return json_files


def get_all_files_in_directory(directory_path):
    """ list and print all files in a directory """
    files_list = []

    for root, _, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            files_list.append(file_path)

    return files_list
