import pandas as pd
import plotly.graph_objects as go


# ---------------------------------------------------------------------------------
# helper functions to create historic data plots
# ---------------------------------------------------------------------------------

# plot gas prices and cryptocurrency token prices
def plot_historic_network_data(data_dict: dict, title: str, y_axis_title: str, metric: str = "gasPrice",
                               metric_type: str = "low", show_plot: bool = True
                               ):
    # Initialize an empty figure
    historic_figure = go.Figure()

    # Loop through each key-value pair in the data dictionary
    for key, value in data_dict.items():
        # Convert the value (which is a list of dictionaries) into a DataFrame
        df = pd.DataFrame(value['candles'])

        # Convert the 'timestamp' column to datetime objects
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        # Create a new column 'y_value' in the DataFrame by extracting the specified metric type from the metric column
        df['y_value'] = pd.DataFrame(df[metric].apply(lambda x: x[metric_type]))

        # Add a trace to the figure for each key-value pair in the data dictionary
        historic_figure.add_trace(go.Scatter(x=df['timestamp'], y=df['y_value'], mode='lines', text=key, name=key))

    # Update the layout of the figure with the title, axis titles, and dimensions
    historic_figure.update_layout(
        title={
            'text': title,  # Title of the plot
            'x': 0.5,  # X-position of the title (0.5 means centered)
            'xanchor': 'center',  # X-anchor of the title (centered)
            'yanchor': 'top'  # Y-anchor of the title (at the top)
        },
        xaxis_title='Date',
        yaxis_title=y_axis_title,
        autosize=False,
        width=800,
        height=500,
    )

    # Show the plot
    if show_plot:
        historic_figure.show()

    # Return the figure
    return historic_figure


# plot gas costs based on passed gas used value
def plot_historic_network_data_gas_cost(data_dict: dict, y_axis_title: str, gas_used_baseline: int, contract_name: str,
                                        metric_name: str,
                                        metric_type: str = "low", show_plot: bool = True
                                        ):
    historic_figure = go.Figure()

    for key, value in data_dict.items():
        df = pd.DataFrame(value['candles'])
        # Convert the 'timestamp' column to datetime objects
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['gas_price_in_gwei'] = pd.DataFrame(df["gasPrice"].apply(lambda x: x[metric_type]))
        # calculate gas costs based on gas used baseline
        df['gas_price_in_gwei'] = df['gas_price_in_gwei'].astype(float)
        df['gas_costs_in_gwei'] = df['gas_price_in_gwei'].apply(lambda x: x * gas_used_baseline)

        historic_figure.add_trace(
            go.Scatter(x=df['timestamp'], y=df['gas_costs_in_gwei'], mode='lines', text=key,
                       name=key))

    historic_figure.update_layout(
        title={
            'text': f"Gas Costs ({metric_type.title()}) in Gwei for {metric_name.title()} of {contract_name.title()} per Chain per Day Over Time",
            'x': 0.5,
            'font': {
                'size': 12
            },
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title='Date',
        yaxis_title=y_axis_title.title(),
        autosize=False,
        width=800,
        height=500,
    )

    # Show the plot
    if show_plot:
        historic_figure.show()

    return historic_figure


# plot fiat costs based on passed gas used value
def plot_historic_network_data_fiat_cost(data_dict: dict, y_axis_title: str, gas_used_baseline: int, contract_name: str,
                                         metric_name: str,
                                         metric_type: str = "low", show_plot: bool = True
                                         ):
    historic_figure = go.Figure()

    for key, value in data_dict.items():
        df = pd.DataFrame(value['candles'])
        # Convert the 'timestamp' column to datetime objects
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['gas_price_in_gwei'] = pd.DataFrame(df["gasPrice"].apply(lambda x: x[metric_type]))

        df['usd_price_in_gwei'] = pd.DataFrame(df["tokenPrice"].apply(lambda x: x[metric_type] / 1e9))
        # calculate fiat costs based on gas used baseline
        df['gas_price_in_gwei'] = df['gas_price_in_gwei'].astype(float)
        df['gas_costs_in_gwei'] = df['gas_price_in_gwei'].apply(lambda x: x * gas_used_baseline)
        df['fiat_costs_in_usd'] = df['gas_costs_in_gwei'] * df["usd_price_in_gwei"]

        historic_figure.add_trace(go.Scatter(x=df['timestamp'], y=df['fiat_costs_in_usd'], mode='lines', text=key,
                                             name=key))

    historic_figure.update_layout(
        title={
            'text': f"Fiat Costs ({metric_type.title()}) in USD for {metric_name.title()} of {contract_name.title()} per Chain per Day Over Time",
            'x': 0.5,
            'font': {
                'size': 12
            },
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title='Date',
        yaxis_title=y_axis_title.title(),
        autosize=False,
        width=800,
        height=500,
    )

    # Show the plot
    if show_plot:
        historic_figure.show()

    return historic_figure
