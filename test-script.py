# main.py
import pandas as pd

from helpers.create_transaction_plots import create_bar_plot
from helpers.get_data_files_helpers import get_all_json_files
# local imports
from helpers.load_json_data import load_json_data
from helpers.save_visualizations import save_visualization_figure

# PATH CONFIGURATION
evaluation_path = '../logs/evaluations/'
hardhat_path = 'Hardhat-Local_31337/'

# CONTRACT SPECIFIC PATH
contract_type_path = 'referral-payment-multilevel-rewards/'
json_file_name = 'V1ReferralMultilevelRewardsUpgradable-contract-evaluation.json'
contract_name = 'V1ReferralMultilevelRewardsUpgradable'

# create the final file path
file_path = evaluation_path + contract_type_path + hardhat_path + json_file_name

all_files = get_all_json_files(evaluation_path)
print(all_files)

try:
    print("\nExecuting Visualization Script for {}... \n...".format(contract_name)),
    # get all evaluation files
    all_evaluation_file_paths = get_all_json_files(evaluation_path)
    # get evaluation data form json
    evaluation_data: list = load_json_data(file_path)
    number_of_evaluation_runs = len(evaluation_data)
    print("... number of evaluation runs for {} = {}".format(json_file_name, str(number_of_evaluation_runs)))

    # get data frame of evaluation objects
    df_evaluation_data = pd.DataFrame(evaluation_data)

    transaction_data_df_list = []
    number_of_users_in_evaluation_runs_list = []

    print("... extracting transaction data from {} evaluation runs in {}".format(str(number_of_evaluation_runs),
                                                                                 json_file_name))
    for index, item in enumerate(evaluation_data):
        # generate transaction data frames out of the evaluation data
        number_of_users_in_evaluation_runs_list.append(item['numberOfUsers'])
        transaction_data_df_list.append(pd.DataFrame(item['data']))
        # TODO: create evaluation visualizations

    # create plots for tx data
    for index, extracted_tx_data_df in enumerate(transaction_data_df_list):
        number_of_users = number_of_users_in_evaluation_runs_list[
            index]
        print(
            "... generating transaction data visualizations for {} evaluation run with {} users".format(str(index + 1),
                                                                                                        number_of_users))
        # get visualization values
        column_values = extracted_tx_data_df.columns
        x_axis_values = ['txIndex', 'userIteration', 'userTxIteration']
        y_axis_values = list(set(column_values) - set(x_axis_values))
        for x_axis_value in x_axis_values:
            for y_axis_value in y_axis_values:
                plot_title = "{} per {} for {}".format(y_axis_value, x_axis_value, contract_name)
                x_axis_title = x_axis_value
                y_axis_title = y_axis_value

                bar_plot_visualization = create_bar_plot(df=extracted_tx_data_df, x_axis=x_axis_value,
                                                         y_axis=y_axis_value,
                                                         title=plot_title,
                                                         x_axis_title=x_axis_title, y_axis_title=y_axis_title)
                # resulting file name
                result_vis_file_name = "{}-users-{}-per-{}-{}".format(str(number_of_users), y_axis_value,
                                                                      x_axis_value,
                                                                      contract_name)
                bar_vis_file_folder = '{}/plots-for-{}-users/{}'.format(contract_name, number_of_users,
                                                                        y_axis_value) + '/' + 'bar-plots' + '/'

                # save bar plot visualization
                save_visualization_figure(fig=bar_plot_visualization, file_name=result_vis_file_name,
                                          base_folder='tx-visualizations',
                                          file_folder=bar_vis_file_folder)


except FileNotFoundError:
    print(f"Error: The specified evaluation JSON file '{file_path}' does not exist.")
