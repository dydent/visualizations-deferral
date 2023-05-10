# local imports
from helpers.evaluation_run_helpers.extract_contract_path_info import extract_contract_path_info
from helpers.get_data_files_helpers import load_json_data, get_all_json_files
from helpers.overall_evaluation_helpers.create_overall_plots import create_overall_metric_plot, \
    create_grouped_overall_multiple_metrics_plot
from helpers.overall_evaluation_helpers.generate_overall_metrics_table import generate_overall_latex_table
from helpers.overall_evaluation_helpers.unit_converter import wei_to_gwei
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
fiat_cost_metric_keys = list(filter(lambda x: "FiatCost" in x, all_metrics_keys))
gas_cost_metric_keys = list(filter(lambda x: "GasCost" in x, all_metrics_keys))
metric_types = ["avg", "min", "max", "sum"]

# create overall visualizations for a single metric for all metric types
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

# create overall metric tables for all fiat costs metrics of all different chains AND of all (individual) metric
# types--> e.g. gas costs get all gas costs metrics
for metric_type in metric_types:
    file_name = f"overall_{metric_type}_fiat_cost_table_for_{number_of_users}_users"
    base_folder = "overall/tables/fiat-costs"
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

# create overall metric tables for all fiat gas cost metrics of all different chains AND of all (individual) metric
# types--> e.g. fiat costs get all fiat costs metrics
for metric_type in metric_types:
    file_name = f"overall_{metric_type}_gas_cost_table_for_{number_of_users}_users"
    base_folder = "overall/tables/gas-costs"
    rounded_decimal = 3
    table_caption = f"{metric_type} Gas Costs in Gwei Rounded to {rounded_decimal} Decimals Across all Contract " \
                    f"Evaluations with {number_of_users} Users for " \
                    f"All Evaluation Chains"
    table_caption = table_caption[0].upper() + table_caption[1:]

    table_label = f"tab:overall_{metric_type}_gas_costs_for_{number_of_users}_users"
    overall_metrics_table = generate_overall_latex_table(data_array=all_contracts_third_evaluation_runs,
                                                         metric_keys=gas_cost_metric_keys,
                                                         tabel_caption=table_caption,
                                                         table_label=table_label, metric_type=metric_type,
                                                         conversion_fn=wei_to_gwei)
    save_table(overall_metrics_table, file_name=file_name,
               base_folder=base_folder,
               file_folder=metric_type)

# filter out V1ReferralMultilevelRewardsUpgradable outlier
filtered_contract_value = "V1ReferralMultilevelRewardsUpgradable"
filtered_third_evaluation_run_data = list(
    filter(lambda item: item['contractName'] != filtered_contract_value,
           all_contracts_third_evaluation_runs))

# # create overall grouped visualizations for a group of metrics for one metric type

# filter out ethereum high value
filtered_fiat_cost_value = "ethereumFiatCost"
filtered_fiat_cost_metrics = list(filter(lambda x: filtered_fiat_cost_value not in x, fiat_cost_metric_keys))
filtered_gas_cost_value = "goerliGasCost"
filtered_gas_cost_metrics = list(filter(lambda x: filtered_gas_cost_value not in x, gas_cost_metric_keys))

# ---------------------------------------------------------------------------------
# create grouped overall visualizations for fiat costs
# ---------------------------------------------------------------------------------
all_fiat_costs_figure_title = f"fiat_costs_overall_grouped_metrics_{number_of_users}_users"
overall_grouped_fiat_cost_metrics_figure = create_grouped_overall_multiple_metrics_plot(
    all_contracts_third_evaluation_runs, fiat_cost_metric_keys, metrics_title=f"Fiat Costs (USD)")
overall_grouped_fiat_cost_metrics_figure.show()
save_visualization_figure(fig=overall_grouped_fiat_cost_metrics_figure,
                          file_name=all_fiat_costs_figure_title,
                          base_folder="overall/grouped-fiat-costs",
                          file_folder="")

# create FILTERED CONTRACT grouped overall visualizations for fiat costs
filtered_fiat_costs_figure_title = f"contract_filtered_fiat_costs_overall_grouped_metrics_{number_of_users}_users"

filtered_overall_grouped_fiat_cost_metrics_figure = create_grouped_overall_multiple_metrics_plot(
    filtered_third_evaluation_run_data, fiat_cost_metric_keys, metrics_title=f"Fiat Costs (USD)")
save_visualization_figure(fig=filtered_overall_grouped_fiat_cost_metrics_figure,
                          file_name=filtered_fiat_costs_figure_title,
                          base_folder="overall/grouped-fiat-costs",
                          file_folder=f"filtered-{filtered_contract_value}-contract-excluded")

# create DOUBLE FILTERED CONTRACT & ETHEREUM FIAT PRICE grouped overall visualizations for fiat costs
double_filtered_fiat_costs_figure_title = f"double-contract_filtered_fiat_costs_overall_grouped_metrics_{number_of_users}_users"
double_filtered_overall_grouped_fiat_cost_metrics_figure = create_grouped_overall_multiple_metrics_plot(
    filtered_third_evaluation_run_data, filtered_fiat_cost_metrics, metrics_title=f"Fiat Costs (USD)")
save_visualization_figure(fig=double_filtered_overall_grouped_fiat_cost_metrics_figure,
                          file_name=double_filtered_fiat_costs_figure_title,
                          base_folder="overall/grouped-fiat-costs",
                          file_folder=f"filtered-{filtered_contract_value}-contract-excluded/{filtered_fiat_cost_value}-excluded")

# ---------------------------------------------------------------------------------
# create grouped overall visualizations for gas costs
# ---------------------------------------------------------------------------------
all_gas_costs_figure_title = f"gas_costs_overall_grouped_metrics_{number_of_users}_users"
overall_grouped_gas_cost_metrics_figure = create_grouped_overall_multiple_metrics_plot(
    all_contracts_third_evaluation_runs, gas_cost_metric_keys, metrics_title=f"Gas Costs (Gwei)",
    conversion_fn=wei_to_gwei)
overall_grouped_gas_cost_metrics_figure.show()
save_visualization_figure(fig=overall_grouped_gas_cost_metrics_figure,
                          file_name=all_gas_costs_figure_title,
                          base_folder="overall/grouped-gas-costs",
                          file_folder="")
# create FILTERED CONTRACT grouped overall visualizations for gas costs
filtered_overall_grouped_gas_cost_metrics_figure_title = f"contract_filtered_gas_costs_overall_grouped_metrics_{number_of_users}_users"

filtered_overall_grouped_gas_cost_metrics_figure = create_grouped_overall_multiple_metrics_plot(
    filtered_third_evaluation_run_data, gas_cost_metric_keys, metrics_title=f"Gas Costs (Gwei)",
    conversion_fn=wei_to_gwei)
save_visualization_figure(fig=filtered_overall_grouped_gas_cost_metrics_figure,
                          file_name=filtered_overall_grouped_gas_cost_metrics_figure_title,
                          base_folder="overall/grouped-gas-costs",
                          file_folder=f"filtered-{filtered_contract_value}-contract-excluded")

# create DOUBLE FILTERED CONTRACT & ETHEREUM GAS PRICE grouped overall visualizations for gas costs
double_filtered_overall_grouped_gas_cost_metrics_figure_title = f"double_contract_filtered_gas_costs_overall_grouped_metrics_{number_of_users}_users"

double_filtered_overall_grouped_gas_cost_metrics_figure = create_grouped_overall_multiple_metrics_plot(
    filtered_third_evaluation_run_data, filtered_gas_cost_metrics, metrics_title=f"Gas Costs (Gwei)",
    conversion_fn=wei_to_gwei)
save_visualization_figure(fig=double_filtered_overall_grouped_gas_cost_metrics_figure,
                          file_name=double_filtered_overall_grouped_gas_cost_metrics_figure_title,
                          base_folder="overall/grouped-gas-costs",
                          file_folder=f"filtered-{filtered_contract_value}-contract-excluded/{filtered_gas_cost_value}-excluded")
