import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

from helpers.convert_string_to_number import convert_string_to_number


def create_single_evaluation_metric_type_bar_plot(evaluation_data: list, metric_value: str, metric_type: str,
                                                  plot_title: str,
                                                  html_output: bool = False):
    # arrange data --> extract metric values for type and ids
    values = [convert_string_to_number(entry["metrics"][metric_value][metric_type]) for entry in evaluation_data]
    number_of_user_values = [entry["numberOfUsers"] for entry in evaluation_data]
    ids = [entry["id"] + 1 for entry in evaluation_data]

    # Create a bar chart
    fig = go.Figure()
    fig.add_trace(go.Bar(x=ids, y=values, name='Average', text=values, textposition='auto'))

    # Add text labels for numberOfUsers on top of each bar group
    annotations = []
    extra_space = 0.1  # Define extra space between annotations and bars

    for i, id_value in enumerate(ids):
        max_value = max(values)
        annotations.append(
            go.layout.Annotation(text=f'Users: {number_of_user_values[i]}', x=id_value, y=max_value * (1 + extra_space),
                                 showarrow=False, font=dict(size=18)))

    fig.update_layout(
        title=plot_title,
        title_x=0.5,  # Center the title
        xaxis=dict(title='Evaluation Run'),
        yaxis=dict(title=str.title(f'{metric_type} {metric_value}')),
        barmode='group',
        legend=dict(
            font=dict(
                size=16,  # Increase the font size of the legend
            )
        ),
        annotations=annotations,  # Add the annotations to the layout

    )

    # show and output chart
    if html_output:
        fig.write_html('{}.html'.format(plot_title), auto_open=True)
        fig.show()
    #  return plot
    return fig


def create_grouped_evaluation_metric_values_bar_plot(evaluation_data: list, metric_value: str, plot_title: str,
                                                     html_output: bool = False):
    # arrange data --> extract metric values and ids
    avg_values = [convert_string_to_number(entry["metrics"][metric_value]["avg"]) for entry in evaluation_data]
    median_values = [convert_string_to_number(entry["metrics"][metric_value]["median"]) for entry in evaluation_data]
    min_values = [convert_string_to_number(entry["metrics"][metric_value]["min"]) for entry in evaluation_data]
    max_values = [convert_string_to_number(entry["metrics"][metric_value]["max"]) for entry in evaluation_data]
    number_of_user_values = [entry["numberOfUsers"] for entry in evaluation_data]
    ids = [entry["id"] + 1 for entry in evaluation_data]

    # Create a bar chart
    fig = go.Figure()
    fig.add_trace(go.Bar(x=ids, y=avg_values, name='Average', text=avg_values, textposition='auto'))
    fig.add_trace(go.Bar(x=ids, y=median_values, name='Median', text=median_values, textposition='auto'))
    fig.add_trace(go.Bar(x=ids, y=min_values, name='Minimum', text=min_values, textposition='auto'))
    fig.add_trace(go.Bar(x=ids, y=max_values, name='Maximum', text=max_values, textposition='auto'))

    # Add text labels for numberOfUsers on top of each bar group
    annotations = []
    extra_space = 0.1  # Define extra space between annotations and bars

    for i, id_value in enumerate(ids):
        max_value = max(avg_values[i], median_values[i], min_values[i], max_values[i], )
        annotations.append(
            go.layout.Annotation(text=f'Users: {number_of_user_values[i]}', x=id_value, y=max_value * (1 + extra_space),
                                 showarrow=False, font=dict(size=18)))

    fig.update_layout(
        title=plot_title,
        title_x=0.5,  # Center the title
        xaxis=dict(title='Evaluation Run '),
        yaxis=dict(title=str.title(metric_value)),
        barmode='group',
        legend=dict(
            font=dict(
                size=16,  # Increase the font size of the legend
            )
        ),
        annotations=annotations,  # Add the annotations to the layout

    )

    # show and output chart
    if html_output:
        fig.write_html('{}.html'.format(plot_title), auto_open=True)
        fig.show()
    #  return plot
    return fig


def create_grouped_evaluation_metric_types_bar_plot(evaluation_data: list, all_metric_values: list, metric_type: str,
                                                    plot_title: str,
                                                    html_output: bool = False):
    fig = go.Figure()

    ids = [entry["id"] + 1 for entry in evaluation_data]
    number_of_user_values = [entry["numberOfUsers"] for entry in evaluation_data]

    all_values = []

    for metric_value in all_metric_values:
        values = [convert_string_to_number(entry["metrics"][metric_value][metric_type]) for entry in evaluation_data]
        all_values.append(values)
        fig.add_trace(
            go.Bar(x=ids, y=values, name=f'{metric_type} {metric_value}', text=f'{metric_value}', textposition='auto'))

    # Add text labels for numberOfUsers on top of each bar group
    annotations = []
    extra_space = 0.1  # Define extra space between annotations and bars

    # for i, id_value in enumerate(ids):
    #     for values in all_values:
    #         max_value = max(values[i])
    #     annotations.append(
    #         go.layout.Annotation(text=f'Users: {number_of_user_values[i]}', x=id_value, y=max_value * (1 + extra_space),
    #                              showarrow=False, font=dict(size=18)))

    fig.update_layout(
        title=plot_title,
        title_x=0.5,  # Center the title
        xaxis=dict(title='Evaluation Run '),
        yaxis=dict(title=str.title(metric_type)),
        barmode='group',
        legend=dict(
            font=dict(
                size=16,  # Increase the font size of the legend
            )
        ),
        # annotations=annotations,  # Add the annotations to the layout

    )

    # show and output chart
    if html_output:
        fig.write_html('{}.html'.format(plot_title), auto_open=True)
        fig.show()
    #  return plot
    return fig
