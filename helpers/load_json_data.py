import pandas as pd
import json
from typing import List
from dataclasses import asdict
from evaluation_classes import EvaluationLogJsonInputType
from typing import Any


def load_json_data(file_path: str) -> list:
    """ function to load a pandas df from a .json data file """
    with open(file_path, "r") as file:
        data: list = json.load(file)

    return data

#
# def load_json_data(file_path: str) -> pd.DataFrame:
#     print(file_path)
#     with open(file_path, "r") as file:
#         data_list = json.load(file)
#
#     # Convert each EvaluationLogJsonInputType object to a dictionary
#     data_dicts: List[dict] = [asdict(EvaluationLogJsonInputType(**data)) for data in data_list]
#
#     # Convert the list of dictionaries to a pandas DataFrame
#     df = pd.DataFrame(data_dicts)
#
#     return df
