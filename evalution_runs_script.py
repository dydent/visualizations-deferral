import sys

import pandas as pd
# local imports
from helpers.convert_to_numbers import convert_to_numbers
from helpers.create_subplot import create_subplot
from helpers.create_transaction_evaluation_bar_chart import create_transaction_bar_chart
from helpers.create_transaction_plots import create_bar_plot, create_scatter_plot
from helpers.create_evaluation_plots import create_grouped_evaluation_metric_values_bar_plot, \
    create_single_evaluation_metric_type_bar_plot, create_grouped_evaluation_metric_types_bar_plot
from helpers.extract_contract_path_info import extract_contract_path_info
from helpers.save_visualizations import save_visualization_figure
from helpers.get_data_files_helpers import load_json_data, get_all_json_files

# ---------------------------------------------------------------------------------
# ANALYSIS SCRIPT FOR TRANSACTION EVALUATION DATA
# ---------------------------------------------------------------------------------


# PATH CONFIGURATION
# path where the deferral evaluation scripts store the json files
# might have to be adapted based on the folder setup
evaluation_log_files_path = '../logs/evaluations/'
# network information on which the evaluation scripts have been executed that is part of the file path
evaluation_network_path = 'Hardhat-Local_31337/'

show_plots = False

print(f"\nExecuting transaction evaluation analysis script...\n...")

# extract all json evaluation files from evaluation directory of
all_contract_evaluation_files = get_all_json_files(evaluation_log_files_path)

# extract needed information from file paths of evaluation files
evaluation_files_contract_info = extract_contract_path_info(all_contract_evaluation_files)

# Loop through the keys and values of the dictionary
for path_value, contracts in evaluation_files_contract_info.items():
    contract_type_path = path_value
    storage_path = "transaction-evaluation"
    for contract in contracts:
        contract_name = contract["contract_name"]
        file_path = contract["full_path"]
        json_file_name = f"{contract_name}.json"

        print(f"\nAnalyzing {json_file_name}...")


