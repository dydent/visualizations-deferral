import pandas as pd
import plotly.graph_objects as go

from helpers.constants.visualization_colors import PLOT_BACKGROUND_COLOR


# ---------------------------------------------------------------------------------
# helper functions to create overall bar chart plot
# ---------------------------------------------------------------------------------

def create_overall_metric_plot(data, metric: str, metric_type: str = "avg"):
    # Extract the 'avg' value from the 'gasUsed' dictionary for each item and convert to a float
    for item in data:
        item['metricValues'] = float(item['metrics'][metric][metric_type])

    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(data)

    # Sort the DataFrame by 'metricValues' in ascending order (lowest to highest)
    df = df.sort_values('metricValues')

    # Create a bar chart using Plotly
    overall_fig = go.Figure(go.Bar(
        x=df['contractName'],
        y=df['metricValues'],
        text=df['metricValues'],
        textposition='auto'
    ))

    # Customize the chart's appearance
    overall_fig.update_layout(
        title=f"{metric_type} {metric} for all Deferral Solution Contracts",
        title_x=0.5,
        xaxis_title='Contract Name',
        yaxis_title=f"{metric_type} {metric}",
        plot_bgcolor=PLOT_BACKGROUND_COLOR,
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightGrey')
    )
    overall_fig.update_xaxes(tickangle=35, tickfont=dict(size=9))

    return overall_fig


def create_grouped_overall_multiple_metrics_plot(data, metrics: list, metrics_title: str, metric_type: str = "avg",
                                                 conversion_fn=None):
    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(data)

    # Extract the 'avg' value from the 'metrics' dictionary for each item and convert to a float
    for metric in metrics:
        df[metric] = df['metrics'].apply(lambda x: float(x[metric][metric_type]))
        if conversion_fn:
            df[metric] = df[metric].apply(conversion_fn)

    # Sort the DataFrame by first metric's values in ascending order (lowest to highest)
    df = df.sort_values(by=metrics[0])

    # Create a bar chart using Plotly
    overall_fig = go.Figure()

    for metric in metrics:
        overall_fig.add_trace(go.Bar(
            x=df['contractName'],
            y=df[metric],
            text=df[metric],
            textposition='auto',
            name=metric
        ))

    title = f"{metric_type} {metrics_title} for Deferral Solution Contracts"
    title = title[0].upper() + title[1:]

    # Customize the chart's appearance
    overall_fig.update_layout(
        title=title,
        title_x=0.5,
        xaxis_title='Contract Name',
        yaxis_title=f"{metric_type.title()} {metrics_title.title()} Metric",
        plot_bgcolor=PLOT_BACKGROUND_COLOR,
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightGrey'),
        barmode='group'
    )
    overall_fig.update_xaxes(tickangle=35, tickfont=dict(size=9))

    return overall_fig
