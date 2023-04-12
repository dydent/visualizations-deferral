import pandas as pd
import plotly.express as px


def create_bar_chart(df: pd.DataFrame, y_axis: str):
    fig = px.bar(df, y=df[y_axis], color=df[y_axis], hover_data=df.columns)

    fig.update_layout(
        title="{} per Tx".format(y_axis),
        title_x=0.5,  # Center the title
        font=dict(size=8),
        xaxis_title="tx iteration",
        yaxis_title="{}".format(y_axis),
    )

    fig.write_html('first_figure.html', auto_open=True)
    fig.show()
    return fig
