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
from helpers.generate_overall_evaluation_run_metric_table import generate_latex_table
from helpers.generate_single_evaluation_run_metric_table import generate_latex_table_single_object, \
    generate_latex_table_with_human_readable_values_v2, generate_latex_table_with_human_readable_values_rounded
from helpers.save_tables import save_table
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

# flag to define if script shows plots
show_plots = False

print(f"\nExecuting evaluation runs evaluation analysis script...\n...")

# extract all json evaluation files from evaluation directory of
all_contract_evaluation_files = get_all_json_files(evaluation_log_files_path)

# extract needed information from file paths of evaluation files
evaluation_files_contract_info = extract_contract_path_info(all_contract_evaluation_files)

# Loop through the keys and values of the dictionary
for path_value, contracts in evaluation_files_contract_info.items():
    contract_type_path = path_value
    storage_path = "evaluation-runs-evaluation"
    for contract in contracts:
        contract_name = contract["contract_name"]
        file_path = contract["full_path"]
        json_file_name = f"{contract_name}.json"
        print(f"\nAnalyzing {json_file_name}...\n...")

        # CONTRACT NAME FOR THE STORED VISUALIZATION FILES

        # try to load and visualize data from generated json evaluation files
        try:
            # get evaluation data from json evaluation file
            evaluation_data: list = load_json_data(file_path)
            evaluation_data_df: pd.DataFrame = pd.DataFrame(evaluation_data)
            number_of_evaluation_runs = len(evaluation_data)

            print(f"... number of evaluation runs for {json_file_name} = {number_of_evaluation_runs}\n...")

            evaluation_metrics_df_list = []
            number_of_users_in_evaluation_runs_list = []
            for index, item in enumerate(evaluation_data):
                # generate transaction data frames out of the evaluation data
                number_of_users_in_evaluation_runs_list.append(item['numberOfUsers'])
                evaluation_metrics_df_list.append(pd.DataFrame(item['metrics']))

            # generate metric tables
            all_metrics_keys = list(evaluation_data[0]["metrics"].keys())

            # create overall metric tables
            # create tables for all metrics across evaluation runs
            for metric in all_metrics_keys:
                table_caption = f"{metric} for Evaluation Runs of {contract_name}"
                table_label = f"tab:{metric}_evaluation_runs_table_for_{contract_name}"

                table_storage_folder = f"{contract_name}/{storage_path}/overall-metric-tables/"
                generated_table = generate_latex_table(evaluation_data, metric, tabel_caption=table_caption,
                                                       table_label=table_label)
                save_table(generated_table, file_name=f"table_{metric}_{contract_name}",
                           base_folder=contract_type_path,
                           file_folder=table_storage_folder)

            # create metric tables per evaluation run
            gas_cost_metric_keys = list(filter(lambda x: "GasCost" in x, all_metrics_keys))
            fiat_cost_metric_keys = list(filter(lambda x: "FiatCost" in x, all_metrics_keys))
            keys_without_gas_and_fiat_costs = list(
                filter(lambda x: "GasCost" and "FiatCost" not in x, all_metrics_keys))

            single_evaluation_metric_keys_list = [gas_cost_metric_keys, fiat_cost_metric_keys]
            print("gas_cost_keys", gas_cost_metric_keys)

            # ---------------------------------------------------------------------------------
            # gas cost tables
            # ---------------------------------------------------------------------------------

            # create gas costs metrics per evaluation run
            for index, evaluation_run_data in enumerate(evaluation_data):
                nr_of_users = number_of_users_in_evaluation_runs_list[index]
                gas_cost_table_caption = f"Gas Costs Metrics (in Wei) for Evaluation with {nr_of_users} of {contract_name}"
                gas_cost_table_label = f"tab:gas_costs_metrics_for_{nr_of_users}_users_for_{contract_name}"
                gas_cost_table_storage_folder = f"{contract_name}/{storage_path}/gas-cost-metric-tables/{nr_of_users}_users/"

                gas_cost_table = generate_latex_table_with_human_readable_values_v2(evaluation_run_data,
                                                                                    gas_cost_metric_keys,
                                                                                    table_caption=gas_cost_table_caption,
                                                                                    table_label=gas_cost_table_label)

                save_table(gas_cost_table, file_name=f"gas_cost_table_for_{nr_of_users}_users_{contract_name}",
                           base_folder=contract_type_path,
                           file_folder=gas_cost_table_storage_folder)

            # ---------------------------------------------------------------------------------
            # fiat cost tables
            # ---------------------------------------------------------------------------------

            # create fiat costs metrics per evaluation run
            for index, evaluation_run_data in enumerate(evaluation_data):
                nr_of_users = number_of_users_in_evaluation_runs_list[index]
                fiat_cost_table_caption = f"Costs Metrics (in USD) for Evaluation with {nr_of_users} of {contract_name}"
                fiat_cost_table_label = f"tab:fiat_costs_metrics_for_{nr_of_users}_users_for_{contract_name}"
                fiat_cost_table_storage_folder = f"{contract_name}/{storage_path}/fiat-cost-metric-tables/{nr_of_users}_users/"

                fiat_cost_table = generate_latex_table_with_human_readable_values_rounded(evaluation_run_data,
                                                                                          fiat_cost_metric_keys,
                                                                                          table_caption=fiat_cost_table_caption,
                                                                                          table_label=fiat_cost_table_label)

                save_table(fiat_cost_table, file_name=f"fiat_cost_table_for_{nr_of_users}_users_{contract_name}",
                           base_folder=contract_type_path,
                           file_folder=fiat_cost_table_storage_folder)

            # print(evaluation_data_df.describe())



        # if the evaluation run evaluation file could not be loaded --> make sure the evaluation scripts have been executed
        except FileNotFoundError:
            print(f"Error: The specified evaluation JSON file '{file_path}' does not exist.")
