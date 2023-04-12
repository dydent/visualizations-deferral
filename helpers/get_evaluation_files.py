import os
from typing import List


def get_all_json_files(directory: str) -> List[str]:
    """ get all json files from a directory and return a list"""
    json_files = []

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                json_files.append(os.path.join(root, file))

    return json_files
