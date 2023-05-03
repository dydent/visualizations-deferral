import pandas as pd
# local imports
from helpers.converters.convert_list_to_numbers import convert_to_numbers
from helpers.create_subplot import create_subplot
from helpers.create_transaction_evaluation_bar_chart import create_transaction_bar_chart
from helpers.extract_contract_path_info import extract_contract_path_info
from helpers.save_visualizations import save_visualization_figure
from helpers.get_data_files_helpers import load_json_data, get_all_json_files

# ---------------------------------------------------------------------------------
# VISUALIZATION SCRIPT FOR V1ReferralPaymentTransmitter EVALUATION DATA
# ---------------------------------------------------------------------------------


# PATH CONFIGURATION
# path where the deferral evaluation scripts store the json files
evaluation_path = '../../../logs/evaluations/'
# network information that is part of the file path
hardhat_path = 'Hardhat-Local_31337/'

all_contract_evaluation_files = get_all_json_files(evaluation_path)
print(all_contract_evaluation_files)

all_contracts = extract_contract_path_info(all_contract_evaluation_files)

# Loop through the keys and values of the dictionary

# Loop through the keys and values of the dictionary


for path_value, contracts in all_contracts.items():
    contract_type_path = path_value

    for contract in contracts:
        contract_name = contract["contract_name"]
        file_path = contract["full_path"]
        json_file_name = f"{contract_name}.json"

        # CONTRACT NAME FOR THE STORED VISUALIZATION FILES

        # try to load and visualize data from generated json evaluation files
        try:
            print(f"\nExecuting Visualization Script for {contract_name}...\n...")

            # get evaluation data from json file
            evaluation_data: list = load_json_data(file_path)
            evaluation_data_df: pd.DataFrame = pd.DataFrame(evaluation_data)
            number_of_evaluation_runs = len(evaluation_data)

            print(f"... number of evaluation runs for {json_file_name} = {json_file_name}\n...")

            # ---------------------------------------------------------------------------------
            # generating tx visualizations per evaluation
            # ---------------------------------------------------------------------------------
            print(
                f"\n... extracting transaction data from {str(number_of_evaluation_runs)} evaluation runs in {json_file_name} for transaction visualizations")

            # empty lists for tx data dataframes and number of users per evaluation run
            transaction_data_df_list = []
            number_of_users_in_evaluation_runs_list = []
            for index, item in enumerate(evaluation_data):
                # generate transaction data frames out of the evaluation data
                number_of_users_in_evaluation_runs_list.append(item['numberOfUsers'])
                transaction_data_df_list.append(pd.DataFrame(item['data']))

            # define transaction metrics that should be visualized
            transaction_metric_values = [{"value": "gasUsed", "title": "Gas Used"},
                                         {"value": "durationInMs", "title": "Duration in MS"},
                                         {"value": "ethereumFiatCost", "title": "Costs (USD) on Ethereum"}]

            for transaction_metric in transaction_metric_values:
                metric_bar_charts = []
                metric_bar_charts_titles = []
                for i, df in enumerate(transaction_data_df_list):
                    bar_chart = create_transaction_bar_chart(
                        y_axis_data=convert_to_numbers(df[transaction_metric["value"]]),
                        x_axis_data=df.index)
                    bar_chart.show()
                    metric_bar_charts.append(bar_chart)
                    metric_bar_charts_titles.append(
                        f"{transaction_metric['title']} for {str(number_of_users_in_evaluation_runs_list[i])} Users")

                gas_used_subplot = create_subplot(figures=metric_bar_charts,
                                                  trace_label=f"{transaction_metric['title']} per TX",
                                                  figure_titles=metric_bar_charts_titles,
                                                  subplot_title=f"{transaction_metric['title']} per Evaluation Run for {str(contract_name)}")
                gas_used_subplot.show()

                save_visualization_figure(fig=gas_used_subplot,
                                          file_name=f"subplot_{transaction_metric['value']}_{contract_name}",
                                          base_folder=contract_type_path,
                                          file_folder=f"{contract_name}/tx-visualizations")

            # ---------------------------------------------------------------------------------
            # generating evaluation visualizations
            # ---------------------------------------------------------------------------------
            print("\n... generating evaluation metric visualizations")

            # create visualizations for evaluation data
            # metric values that should be visualized
            # print(evaluation_data)
            evaluation_metric_value_keys = list(dict(evaluation_data[0]['metrics']).keys())
            gas_cost_keys = list(filter(lambda x: "gasCost" in x, evaluation_metric_value_keys))
            fiat_cost_keys = list(filter(lambda x: "gasCost" in x, evaluation_metric_value_keys))
            gas_used_keys = list(filter(lambda x: "gasUsed" in x, evaluation_metric_value_keys))

            print(evaluation_metric_value_keys)
            eval_columns = evaluation_data_df.metrics

            # metric types that should be visualized
            evaluation_metric_types = ['avg', 'min', 'max', 'median', 'sum']


        except FileNotFoundError:
            print(f"Error: The specified evaluation JSON file '{file_path}' does not exist.")
