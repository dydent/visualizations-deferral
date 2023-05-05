import pandas as pd

# local imports
from helpers.converters.convert_list_to_numbers import convert_to_numbers
from helpers.evaluation_run_helpers.extract_contract_path_info import extract_contract_path_info
from helpers.get_data_files_helpers import load_json_data, get_all_json_files

# ---------------------------------------------------------------------------------
# ANALYSIS SCRIPT FOR TRANSACTION EVALUATION DATA
# ---------------------------------------------------------------------------------


# PATH CONFIGURATION
# path where the deferral evaluation scripts store the json files
# might have to be adapted based on the folder setup
from helpers.save_helpers.save_visualizations import save_visualization_figure
from helpers.transaction_evaluation_helpers.create_subplot import create_subplot
from helpers.transaction_evaluation_helpers.create_transaction_evaluation_bar_chart import create_transaction_bar_chart

evaluation_log_files_path = '../logs/evaluations/'
# network information on which the evaluation scripts have been executed that is part of the file path
evaluation_network_path = 'Hardhat-Local_31337/'

# flag to define if script shows plots
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
        print(f"\nAnalyzing {json_file_name}...\n...")

        # CONTRACT NAME FOR THE STORED VISUALIZATION FILES

        # try to load and visualize data from generated json evaluation files
        try:

            # get evaluation data from json evaluation file
            evaluation_data: list = load_json_data(file_path)
            evaluation_data_df: pd.DataFrame = pd.DataFrame(evaluation_data)
            number_of_evaluation_runs = len(evaluation_data)

            print(f"... number of evaluation runs for {json_file_name} = {number_of_evaluation_runs}\n...")

            # empty lists for tx data dataframes and number of users per evaluation run
            transaction_data_df_list = []
            number_of_users_in_evaluation_runs_list = []

            for index, item in enumerate(evaluation_data):
                # generate transaction data frames out of the evaluation data
                number_of_users_in_evaluation_runs_list.append(item['numberOfUsers'])
                transaction_data_df_list.append(pd.DataFrame(item['data']))

            # define transaction metrics that should be visualized
            # --> values displayed on y-axis
            transaction_metric_values = [{"value": "gasUsed", "title": "Gas Used"},
                                         {"value": "durationInMs", "title": "Duration in MS"},
                                         {"value": "polygonMainnetFiatCost", "title": "Costs (USD) on Polygon"},
                                         {"value": "bscFiatCost", "title": "Costs (USD) on Binance"},
                                         {"value": "arbitrumMainnetFiatCost", "title": "Costs (USD) on Arbitrum"},
                                         {"value": "goerliFiatCost", "title": "Costs (USD) on Goerli"},
                                         {"value": "optimismMainnetFiatCost", "title": "Costs (USD) on Optimism"},
                                         {"value": "avalancheFiatCost", "title": "Costs (USD) on Avalanche"},
                                         {"value": "ethereumFiatCost", "title": "Costs (USD) on Ethereum"}]
            # values that should be used on the x-axis
            x_axis_values = ["TX-ID", "userIteration", "userTxIteration"]

            for x_axis_value in x_axis_values:
                # define values where to store the result files
                storage_x_axis_folder = f"{x_axis_value}"
                if x_axis_value == "TX-ID":
                    storage_x_axis_folder = ""
                storage_base_folder = contract_type_path
                file_storage_folder = f"{contract_name}/{storage_path}/{storage_x_axis_folder}"
                # create visualizations
                for transaction_metric in transaction_metric_values:
                    metric_bar_charts = []
                    metric_bar_charts_titles = []
                    for i, df in enumerate(transaction_data_df_list):
                        # define x axis values to use for chart
                        if x_axis_value == "TX-ID":
                            y_axis_data = df.index
                        else:
                            y_axis_data = convert_to_numbers(df[x_axis_value])
                        # create the bar chart
                        bar_chart = create_transaction_bar_chart(
                            y_axis_data=convert_to_numbers(df[transaction_metric["value"]]),
                            x_axis_data=y_axis_data)
                        # show plots
                        if show_plots:
                            bar_chart.show()
                        # append bar charts to list
                        metric_bar_charts.append(bar_chart)
                        # append bar chart title to list
                        metric_bar_charts_titles.append(
                            f"{transaction_metric['title']} for {str(number_of_users_in_evaluation_runs_list[i])} Users")

                    # create subplot for current tx evaluation metric e.g. gas used
                    metric_subplot = create_subplot(figures=metric_bar_charts,
                                                    x_axes_label=f"{x_axis_value}",
                                                    trace_label=f"{transaction_metric['title']} per {x_axis_value}",
                                                    figure_titles=metric_bar_charts_titles,
                                                    subplot_title=f"{transaction_metric['title']} per Evaluation Run for {str(contract_name)}")
                    # show subplot
                    if show_plots:
                        metric_subplot.show()

                    # save all subplot visualizations
                    save_visualization_figure(fig=metric_subplot,
                                              file_name=f"subplot_{transaction_metric['value']}_{x_axis_value}_{contract_name}",
                                              base_folder=storage_base_folder,
                                              file_folder=file_storage_folder)

        # if the transaction evaluation file could not be loaded --> make sure the evaluation scripts have been executed
        except FileNotFoundError:
            print(f"Error: The specified evaluation JSON file '{file_path}' does not exist.")
