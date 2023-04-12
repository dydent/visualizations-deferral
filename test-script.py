# main.py
import os
import pandas as pd
import plotly.express as px
# local imports
from helpers.load_json_data import load_json_data
from helpers.create_bar_chart import create_bar_chart
from helpers.save_visualizations import save_visualization_figure
from helpers.get_evaluation_files import get_all_json_files

# PATH CONFIGURATION
evaluation_path = '../logs/evaluations/'
hardhat_path = 'Hardhat-Local_31337/'

# CONTRACT SPECIFIC PATH
contract_type_path = 'referral-payment-multilevel-rewards/'
json_file_name = 'V1ReferralMultilevelRewardsUpgradable-contract-evaluation.json'

# create the final file path
file_path = evaluation_path + contract_type_path + hardhat_path + json_file_name

all_files = get_all_json_files(evaluation_path)
print(all_files)

try:
    # get all evaluation files
    all_evaluation_file_paths = get_all_json_files(evaluation_path)
    # get evaluation data form json
    evaluation_data: list = load_json_data(file_path)
    number_of_evaluation_runs = len(evaluation_data)
    print("Number of evaluation runs for {}: {}".format(json_file_name, str(number_of_evaluation_runs)))

    # get data frame of evaluation objects
    df_evaluation_data = pd.DataFrame(evaluation_data)

    # generate transaction data frames out of the evaluation data
    transaction_data_dict = {}
    transaction_data_df_list = []
    for index, item in enumerate(evaluation_data):
        print('index', index)
        print('item', item)
        tx_data = item['data']
        print('tx_data', tx_data)
        print('length of tx data', len(tx_data))
        result = {index: tx_data}
        transaction_data_df_list.append(pd.DataFrame(tx_data))

    example_tx_data_df = transaction_data_df_list[0]
    print('example tx df', example_tx_data_df)

    y_axis = 'durationInMs'
    fig = px.bar(example_tx_data_df, y=example_tx_data_df[y_axis])

    fig.update_layout(
        title="{} per Tx for {}".format(y_axis, json_file_name),
        title_x=0.5,  # Center the title
        font=dict(size=14)
    )

    fig.write_html('first_figure.html', auto_open=True)
    fig.show()

    save_visualization_figure(fig, json_file_name)

    create_bar_chart(example_tx_data_df, 'durationInMs')

    # tx_data_fig = px.bar(example_tx_data_df, y=example_tx_data_df.gasUsed)
    # tx_data_fig.write_html('first_figure.html', auto_open=True)
    #
    # create_bar_chart()
    #
    # print(evaluation_data)
    # print(len(evaluation_data))
    #
    # # Specify the column name for the y-axis of the bar chart
    # y_axis = 'durationInMs'  # Replace this with the desired column name
    #
    # # Create the bar chart
    # evaluation_fig = create_bar_chart(evaluation_df, y_axis)
    #
    # transaction_fig = create_bar_chart(transaction_df, y_axis)

    # Display the bar chart
    # evaluation_fig.show()
    # transaction_fig.show()

    # Save the bar chart as an image in the 'results' folder
    # save_bar_chart(fig, "bar_chart")

except FileNotFoundError:
    print(f"Error: The specified evaluation JSON file '{file_path}' does not exist.")
