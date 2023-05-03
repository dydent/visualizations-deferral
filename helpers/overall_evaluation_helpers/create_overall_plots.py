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
