import pandas as pd
import plotly.graph_objects as go


# ---------------------------------------------------------------------------------
# helper functions to create historic data plots
# ---------------------------------------------------------------------------------

def plot_historic_network_data(data_dict: dict, title: str, y_axis_title: str, metric: str = "gasPrice",
                               metric_type: str = "low",
                               ):
    historic_figure = go.Figure()

    for key, value in data_dict.items():
        df = pd.DataFrame(value['candles'])
        # Convert the 'timestamp' column to datetime objects
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['y_value'] = pd.DataFrame(df[metric].apply(lambda x: x[metric_type]))

        historic_figure.add_trace(go.Scatter(x=df['timestamp'], y=df['y_value'], mode='lines', text=key,
                                             name=key))

    historic_figure.update_layout(
        title={
            'text': title,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title='Date',
        yaxis_title=y_axis_title,
        autosize=False,
        width=800,
        height=500,
    )

    # Show the plot
    historic_figure.show()
    return historic_figure


def plot_historic_network_data_gas_cost(data_dict: dict, y_axis_title: str, gas_used_baseline: int,
                                        metric_type: str = "low",
                                        ):
    historic_figure = go.Figure()

    for key, value in data_dict.items():
        df = pd.DataFrame(value['candles'])
        # Convert the 'timestamp' column to datetime objects
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['gas_price_in_gwei'] = pd.DataFrame(df["gasPrice"].apply(lambda x: x[metric_type]))
        # calculate gas costs based on gas used baseline
        df['gas_costs_in_gwei'] = df['gas_price_in_gwei'].apply(lambda x: x * gas_used_baseline)

        historic_figure.add_trace(
            go.Scatter(x=df['timestamp'], y=df['gas_costs_in_gwei'], mode='lines', text=key,
                       name=key))

    historic_figure.update_layout(
        title={
            'text': f"Gas Costs ({metric_type.title()}) in Gwei Per Chain Per Day Over Time",
            'x': 0.5,
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
    historic_figure.show()
    return historic_figure


def plot_historic_network_data_fiat_cost(data_dict: dict, y_axis_title: str, gas_used_baseline: int,
                                         metric_type: str = "low",
                                         ):
    historic_figure = go.Figure()

    for key, value in data_dict.items():
        df = pd.DataFrame(value['candles'])
        # Convert the 'timestamp' column to datetime objects
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['gas_price_in_gwei'] = pd.DataFrame(df["gasPrice"].apply(lambda x: x[metric_type]))
        df['usd_price_in_gwei'] = pd.DataFrame(df["tokenPrice"].apply(lambda x: x[metric_type] / 1e9))
        # calculate gas costs based on gas used baseline
        df['gas_costs_in_gwei'] = df['gas_price_in_gwei'].apply(lambda x: x * gas_used_baseline)
        df['gas_costs_in_usd'] = df['gas_costs_in_gwei'] * df["usd_price_in_gwei"]

        historic_figure.add_trace(go.Scatter(x=df['timestamp'], y=df['gas_costs_in_usd'], mode='lines', text=key,
                                             name=key))

    historic_figure.update_layout(
        title={
            'text': f"Fiat Costs ({metric_type.title()}) in USD Per Chain Per Day Over Time",
            'x': 0.5,
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
    historic_figure.show()
    return historic_figure
