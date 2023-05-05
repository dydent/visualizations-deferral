# local imports
from helpers.evaluation_run_helpers.extract_contract_path_info import extract_contract_path_info
from helpers.get_data_files_helpers import load_json_data, get_all_json_files
from helpers.overall_evaluation_helpers.create_overall_plots import create_overall_metric_plot
from helpers.overall_evaluation_helpers.generate_overall_metrics_table import generate_overall_latex_table
from helpers.save_helpers.save_tables import save_table
from helpers.save_helpers.save_visualizations import save_visualization_figure

# ---------------------------------------------------------------------------------
# ANALYSIS SCRIPT FOR OVERALL EVALUATION
# ---------------------------------------------------------------------------------


# PATH CONFIGURATION
# path where the deferral evaluation scripts store the json files
# might have to be adapted based on the folder setup


evaluation_log_files_path = '../logs/evaluations/'
# network information on which the evaluation scripts have been executed that is part of the file path
evaluation_network_path = 'Hardhat-Local_31337/'

# flag to define if script shows plots
show_plots = False

print(f"\nExecuting overall evaluation analysis script...\n...")

# extract all json evaluation files from evaluation directory of
all_contract_evaluation_files = get_all_json_files(evaluation_log_files_path)

# extract needed information from file paths of evaluation files
evaluation_files_contract_info = extract_contract_path_info(all_contract_evaluation_files)

all_evaluation_data = []

# Loop through the keys and values of the dictionary
for path_value, contracts in evaluation_files_contract_info.items():
    contract_type_path = path_value
    storage_path = "transaction-evaluation"
    # combine all evaluation data
    for contract in contracts:
        file_path = contract["full_path"]
        # try to load and visualize data from generated json evaluation files
        try:
            # get evaluation data from json evaluation file
            evaluation_data: list = load_json_data(file_path)
            all_evaluation_data.append(evaluation_data)
        # if the transaction evaluation file could not be loaded --> make sure the evaluation scripts have been executed
        except FileNotFoundError:
            print(f"Error: The specified evaluation JSON file '{file_path}' does not exist.")

all_contracts_third_evaluation_runs = []
number_of_users = None

# extract third evaluation runs from all contract evaluation data
for evaluation_data in all_evaluation_data:
    selected_evaluation_run = evaluation_data[2]
    number_of_users = selected_evaluation_run["numberOfUsers"]
    # remove single transaction datas from dict since not needed
    del selected_evaluation_run['data']
    all_contracts_third_evaluation_runs.append(selected_evaluation_run)

all_metrics_keys = all_evaluation_data[0][0]["metrics"].keys()
metric_types = ["avg", "min", "max", "sum"]
# create overall metrics visualizations
for metric_key in all_metrics_keys:
    for metric_type in metric_types:
        file_name = f"overall_{metric_type}_{metric_key}_{str(number_of_users)}_users"
        base_folder = "overall"
        file_folder = f"{metric_key}/{metric_type}/"
        overall_plot = create_overall_metric_plot(all_contracts_third_evaluation_runs, metric=metric_key,
                                                  metric_type=metric_type)
        save_visualization_figure(fig=overall_plot,
                                  file_name=file_name,
                                  base_folder=base_folder,
                                  file_folder=file_folder)

# create overall metric tables for fiat costs of all different chains --> e.g. fiat costs
# get all fiat costs metrics
all_metrics_keys = all_evaluation_data[0][0]["metrics"].keys()
fiat_cost_metric_keys = list(filter(lambda x: "FiatCost" in x, all_metrics_keys))

for metric_type in metric_types:
    file_name = f"overall_{metric_type}_fiat_cost_table_for_{number_of_users}_users"
    base_folder = "overall/tables"
    rounded_decimal = 3
    table_caption = f"{metric_type} Fiat Costs in USD Rounded to {rounded_decimal} Decimals Across all Contract " \
                    f"Evaluations with {number_of_users} Users for " \
                    f"All Evaluation Chains"
    table_caption = table_caption[0].upper() + table_caption[1:]

    table_label = f"tab:overall_{metric_type}_fiat_costs_for_{number_of_users}_users"
    overall_metrics_table = generate_overall_latex_table(data_array=all_contracts_third_evaluation_runs,
                                                         metric_keys=fiat_cost_metric_keys,
                                                         tabel_caption=table_caption,
                                                         table_label=table_label, metric_type=metric_type)
    save_table(overall_metrics_table, file_name=file_name,
               base_folder=base_folder,
               file_folder=metric_type)
