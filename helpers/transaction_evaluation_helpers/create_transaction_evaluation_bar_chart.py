import plotly.graph_objs as go


# ---------------------------------------------------------------------------------
# helper functions to create simple bar chart
# ---------------------------------------------------------------------------------


def create_transaction_bar_chart(y_axis_data: list, x_axis_data: list, ):
    # create bar chart
    fig = go.Figure()
    fig.add_trace(go.Bar(x=x_axis_data, y=y_axis_data))

    #  return plot
    return fig
