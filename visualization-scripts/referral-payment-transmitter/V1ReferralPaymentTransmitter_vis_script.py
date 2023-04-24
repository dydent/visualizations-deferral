import sys

import pandas as pd
# local imports
from helpers.create_transaction_plots import create_bar_plot, create_scatter_plot
from helpers.create_evaluation_plots import create_grouped_evaluation_metric_values_bar_plot, \
    create_single_evaluation_metric_type_bar_plot, create_grouped_evaluation_metric_types_bar_plot
from helpers.save_visualizations import save_visualization_figure
from helpers.get_data_files_helpers import load_json_data

# ---------------------------------------------------------------------------------
# VISUALIZATION SCRIPT FOR V1ReferralPaymentTransmitter EVALUATION DATA
# ---------------------------------------------------------------------------------


# PATH CONFIGURATION
# path where the deferral evaluation scripts store the json files
evaluation_path = '../../../logs/evaluations/'
# network information that is part of the file path
hardhat_path = 'Hardhat-Local_31337/'

# CONTRACT SPECIFIC PATH

#  TODO make this generic and importable or check at least
contract_type_path = 'referral-payment-transmitter/'
json_file_name = 'V1ReferralPaymentTransmitter-contract-evaluation.json'
# create the final file path
file_path = evaluation_path + contract_type_path + hardhat_path + json_file_name

# CONTRACT NAME FOR THE STORED VISUALIZATION FILES
contract_name = 'V1ReferralPaymentTransmitter'

# try to load and visualize data from generated json evaluation files
try:
    print(f"\nExecuting Visualization Script for {contract_name}...\n...")

    # get evaluation data from json file
    evaluation_data: list = load_json_data(file_path)
    evaluation_data_df: pd.DataFrame = pd.DataFrame(evaluation_data)
    number_of_evaluation_runs = len(evaluation_data)

    print(f"... number of evaluation runs for {json_file_name} = {json_file_name}\n...")

    # ---------------------------------------------------------------------------------
    # generating evaluation visualizations
    # ---------------------------------------------------------------------------------
    print("\n... generating evaluation metric visualizations")

    # create visualizations for evaluation data
    # metric values that should be visualized
    print(evaluation_data)
    evaluation_metric_value_keys = list(dict(evaluation_data[0]['metrics']).keys())
    gas_cost_keys = list(filter(lambda x: "gasCost" in x, evaluation_metric_value_keys))
    fiat_cost_keys = list(filter(lambda x: "gasCost" in x, evaluation_metric_value_keys))
    gas_used_keys = list(filter(lambda x: "gasUsed" in x, evaluation_metric_value_keys))

    print(evaluation_metric_value_keys)
    eval_columns = evaluation_data_df.metrics

    # metric types that should be visualized
    evaluation_metric_types = ['avg', 'min', 'max', 'median', 'sum']

    # create visualizations grouped by metric values
    for metric_value in gas_used_keys:
        print(f"... evaluation {metric_value} visualizations")
        file_folder = f'{contract_type_path}{contract_name}/metric-values/{metric_value}/'
        # create and store files per metric and metric type:
        for metric_type in evaluation_metric_types:
            metric_type_vis_title = f'{metric_type} {metric_value} per Evaluation Run for {contract_name}'
            # create plot
            bar_plot_evaluation_metric_visualization = create_single_evaluation_metric_type_bar_plot(
                evaluation_data=evaluation_data, metric_value=metric_value, metric_type=metric_type,
                plot_title=metric_type_vis_title)
            # get file name and path for storage
            metric_vis_file_name = f'{metric_type}-{metric_value}-{contract_name}'
            # save metric and metric type bar plot visualization
            save_visualization_figure(fig=bar_plot_evaluation_metric_visualization, file_name=metric_vis_file_name,
                                      base_folder='evaluation-visualizations',
                                      file_folder=file_folder)

        # create and store visualization for metric value with all metric types combined
        combined_metric_vis_title = f"{metric_value} Metrics per Evaluation Run for {contract_name}"
        # get file name and path for storage
        combined_metric_vis_file_name = f'combined-{metric_value}-metric-types-{contract_name}'
        # create plot
        bar_plot_combined_evaluation_metric_visualization = create_grouped_evaluation_metric_values_bar_plot(
            evaluation_data=evaluation_data, metric_value=metric_value,
            plot_title=combined_metric_vis_title)
        # save metric with combined metric type bar plot visualization
        save_visualization_figure(fig=bar_plot_combined_evaluation_metric_visualization,
                                  file_name=combined_metric_vis_file_name,
                                  base_folder='evaluation-visualizations',
                                  file_folder=file_folder)

    print("\n... generating evaluation metric visualizations")

    # sys.exit()

    # create visualizations grouped by metric types
    for metric_type in evaluation_metric_types:
        print(f"... evaluation {metric_type} visualizations")
        file_folder = f'{contract_type_path}{contract_name}/metric-types/{metric_type}/'
        # create and store files per metric and metric type:
        for metric_value in evaluation_metric_value_keys:
            metric_type_vis_title = f'{metric_type} {metric_value} per Evaluation Run for {contract_name}'
            # create plot
            bar_plot_evaluation_metric_visualization = create_single_evaluation_metric_type_bar_plot(
                evaluation_data=evaluation_data, metric_value=metric_value, metric_type=metric_type,
                plot_title=metric_type_vis_title)
            # get file name and path for storage
            metric_vis_file_name = f'{metric_type}-{metric_value}-{contract_name}'
            # save metric and metric type bar plot visualization
            save_visualization_figure(fig=bar_plot_evaluation_metric_visualization, file_name=metric_vis_file_name,
                                      base_folder='evaluation-visualizations',
                                      file_folder=file_folder)

        # create and store visualization for metric value with all metric types combined
        combined_metric_vis_title = f"{metric_type} Metrics per Evaluation Run for {contract_name}"
        # get file name and path for storage
        combined_metric_vis_file_name = f'combined-{metric_type}-metric-values-{contract_name}'
        # create plot
        bar_plot_combined_evaluation_metric_visualization = create_grouped_evaluation_metric_types_bar_plot(
            evaluation_data=evaluation_data, all_metric_values=evaluation_metric_value_keys, metric_type=metric_type,
            plot_title=combined_metric_vis_title)
        # save metric with combined metric type bar plot visualization
        save_visualization_figure(fig=bar_plot_combined_evaluation_metric_visualization,
                                  file_name=combined_metric_vis_file_name,
                                  base_folder='evaluation-visualizations',
                                  file_folder=file_folder)

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

    # create plots for tx data
    for index, extracted_tx_data_df in enumerate(transaction_data_df_list):
        number_of_users = number_of_users_in_evaluation_runs_list[
            index]
        print(
            f"\n... generating transaction data visualizations for {str(index + 1)} evaluation run with {number_of_users} users")
        # get values that should be used for transaction visualizations
        tx_data_column_values = extracted_tx_data_df.columns
        tx_data_x_axis_values = ['txIndex', 'userIteration', 'userTxIteration']
        tx_data_y_axis_values = list(set(tx_data_column_values) - set(tx_data_x_axis_values))
        tx_data_y_axis_values = list(filter(lambda x: "gasUsed" in x, tx_data_y_axis_values))

        # create all visualizations
        for x_axis_value in tx_data_x_axis_values:
            for y_axis_value in tx_data_y_axis_values:
                plot_title = f"{y_axis_value} per {x_axis_value} for {contract_name}"
                x_axis_title = x_axis_value
                y_axis_title = y_axis_value
                # create bar plot
                bar_plot_tx_visualization = create_bar_plot(df=extracted_tx_data_df, x_axis=x_axis_value,
                                                            y_axis=y_axis_value,
                                                            title=plot_title,
                                                            x_axis_title=x_axis_title, y_axis_title=y_axis_title)
                # get file name and path for storage
                result_vis_file_name = f"{str(number_of_users)}-users-{y_axis_value}-per-{x_axis_value}-{contract_name}"
                bar_vis_file_folder = f'{contract_type_path}{contract_name}/plots-for-{number_of_users}-users/{y_axis_value}/bar-plots/'
                # save bar plot visualization
                save_visualization_figure(fig=bar_plot_tx_visualization, file_name=result_vis_file_name,
                                          base_folder='tx-visualizations',
                                          file_folder=bar_vis_file_folder)
                # # create scatter plot
                # scatter_plot_tx_visualization = create_scatter_plot(df=extracted_tx_data_df, x_axis=x_axis_value,
                #                                                     y_axis=y_axis_value,
                #                                                     title=plot_title,
                #                                                     x_axis_title=x_axis_title,
                #                                                     y_axis_title=y_axis_title)
                # scatter_vis_file_folder = f'{contract_type_path}{contract_name}/plots-for-{number_of_users}-users/{y_axis_value}/scatter-plots/'
                # # save scatter plot visualization
                # save_visualization_figure(fig=scatter_plot_tx_visualization, file_name=result_vis_file_name,
                #                           base_folder='tx-visualizations',
                #                           file_folder=scatter_vis_file_folder)

except FileNotFoundError:
    print(f"Error: The specified evaluation JSON file '{file_path}' does not exist.")
