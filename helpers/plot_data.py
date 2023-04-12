# helpers/plot_data.py
import plotly.express as px
import pandas as pd


#
# def create_bar_chart(df: pd.DataFrame, y_axis: str) -> None:
#     fig = px.bar(df, y=y_axis)
#     fig.show()

def create_bar_chart(df: pd.DataFrame, y_axis: str):
    fig = px.bar(df, y=df[y_axis])
    fig.write_html('first_figure.html', auto_open=True)
    return fig
