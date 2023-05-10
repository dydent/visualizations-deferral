# local imports
from helpers.evaluation_run_helpers.extract_contract_path_info import extract_contract_path_info
from helpers.get_data_files_helpers import get_all_json_files, load_json_data
from helpers.historic_evaluation_helpers.create_historic_plots import plot_historic_network_data, \
    plot_historic_network_data_gas_cost, plot_historic_network_data_fiat_cost
from helpers.historic_evaluation_helpers.extract_baseline_gas_used_values import extract_baseline_gas_used_values
from helpers.historic_evaluation_helpers.fetch_historic_gas_prices import fetch_historic_gas_prices
from helpers.save_helpers.save_visualizations import save_visualization_figure

# ---------------------------------------------------------------------------------
# ANALYSIS SCRIPT FOR HISTORIC GAS PRICE EVALUATION
# ---------------------------------------------------------------------------------

print(f"\nExecuting historic evaluation analysis script...\n...")

# define the networks for which the historic data should be fetched
evaluation_networks = ["eth", "bsc", "arb", "avax", "poly", "opt"]

# define the metric that should be used
historic_metric_type = "low"

# fetch data
historic_gas_price_data = fetch_historic_gas_prices(networks=evaluation_networks)

# ---------------------------------------------------------------------------------
# HISTORIC GAS PRICES
# ---------------------------------------------------------------------------------
gas_prices_figure_title = f"Gas Prices ({historic_metric_type.title()}) in Gwei per Chains per Day Over Time"
gas_prices_figure_name = f"historic_{historic_metric_type}_gas_prices_over_time"
gas_prices_figure = plot_historic_network_data(historic_gas_price_data,
                                               title=gas_prices_figure_title,
                                               y_axis_title=f"Gas Price ({historic_metric_type.title()}) "
                                                            f"in Gwei",
                                               metric="gasPrice", metric_type=historic_metric_type)
save_visualization_figure(fig=gas_prices_figure,
                          file_name=gas_prices_figure_name,
                          base_folder="historical/gas-prices",
                          file_folder=f"")

# ---------------------------------------------------------------------------------
# HISTORIC TOKEN / FIAT PRICES (IN USD)
# ---------------------------------------------------------------------------------
token_prices_figure_title = f"Cryptocurrency Prices ({historic_metric_type.title()}) in USD per Chains per Day Over Time"
token_prices_figure_name = f"historic_{historic_metric_type}_token_currency_prices_over_time"
token_prices_figure = plot_historic_network_data(historic_gas_price_data,
                                                 title=token_prices_figure_title,
                                                 y_axis_title=f"Cryptocurrency Price ({historic_metric_type.title()}) in USD",
                                                 metric="tokenPrice", metric_type=historic_metric_type)
save_visualization_figure(fig=token_prices_figure,
                          file_name=token_prices_figure_name,
                          base_folder="historical/cryptocurrency-prices",
                          file_folder=f"")

# ---------------------------------------------------------------------------------
# ARRANGE AND EXTRACT RESULT DATA FROM EVALUATION
# ---------------------------------------------------------------------------------
evaluation_log_files_path = '../logs/evaluations/'
# network information on which the evaluation scripts have been executed that is part of the file path
evaluation_network_path = 'Hardhat-Local_31337/'
# extract all json evaluation files from evaluation directory of
all_contract_evaluation_files = get_all_json_files(evaluation_log_files_path)
# extract needed information from file paths of evaluation files
evaluation_files_contract_info = extract_contract_path_info(all_contract_evaluation_files)
all_evaluation_data = []
# Loop through the keys and values of the dictionary
for path_value, contracts in evaluation_files_contract_info.items():
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
# result data
all_contracts_third_evaluation_runs = []
number_of_users = None

# extract third evaluation runs from all contract evaluation data
for evaluation_data in all_evaluation_data:
    selected_evaluation_run = evaluation_data[2]
    number_of_users = selected_evaluation_run["numberOfUsers"]
    # remove single transaction datas from dict since not needed
    del selected_evaluation_run['data']
    all_contracts_third_evaluation_runs.append(selected_evaluation_run)

# get baseline data
baseline_data = extract_baseline_gas_used_values(all_contracts_third_evaluation_runs)

# create gas used value dependent charts
for contract_name, values in baseline_data.items():
    # ---------------------------------------------------------------------------------
    # HISTORIC GAS COSTS with custom gas used baseline from results USING GAS USED BASELINE VALUES
    # ---------------------------------------------------------------------------------
    gas_costs_figure_title = f"Gas Costs ({historic_metric_type.title()}) in Gwei per Chains per Day Over Time"
    gas_cost_figure_name = f"{contract_name}_{values['gas_used_metric_name']}_historic_{historic_metric_type}_gas_costs_over_time"

    gas_cost_figure = plot_historic_network_data_gas_cost(historic_gas_price_data,
                                                          y_axis_title=f"Gas Costs ({historic_metric_type.title()}) in Gwei",
                                                          metric_name=values['gas_used_metric_name'],
                                                          contract_name=contract_name,
                                                          metric_type=historic_metric_type,
                                                          gas_used_baseline=values['gas_used_baseline_value'])
    save_visualization_figure(fig=gas_cost_figure,
                              file_name=gas_cost_figure_name,
                              base_folder="historical/gas-costs",
                              file_folder=f"")

    # ---------------------------------------------------------------------------------
    # HISTORIC FIAT COSTS with custom gas used baseline from results in USD USING GAS USED BASELINE VALUES
    # ---------------------------------------------------------------------------------
    fiat_costs_figure_title = f"Fiat Costs ({historic_metric_type.title()}) in USD per Chains per Day Over Time"
    fiat_cost_figure_name = f"{contract_name}_{values['gas_used_metric_name']}_historic_{historic_metric_type}_fiat_costs_over_time"

    fiat_cost_figure = plot_historic_network_data_fiat_cost(historic_gas_price_data,
                                                            y_axis_title="Costs (USD)",
                                                            metric_name=values['gas_used_metric_name'],
                                                            contract_name=contract_name,
                                                            metric_type=historic_metric_type,
                                                            gas_used_baseline=values['gas_used_baseline_value'])
    save_visualization_figure(fig=fiat_cost_figure,
                              file_name=fiat_cost_figure_name,
                              base_folder="historical/fiat-costs",
                              file_folder=f"")
