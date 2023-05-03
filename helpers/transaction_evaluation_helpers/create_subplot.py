import plotly.subplots as sp
from helpers.constants.visualization_colors import BAR_COLOR, PLOT_BACKGROUND_COLOR


# ---------------------------------------------------------------------------------
# helper functions to create subplot visualization
# ---------------------------------------------------------------------------------


def create_subplot(figures: list, trace_label: str, x_axes_label: str, figure_titles: list, subplot_title: str):
    num_figs = len(figures)

    # Create a subplot with 1 row and as many columns as there are figures
    subplot_fig = sp.make_subplots(rows=1, cols=num_figs, subplot_titles=figure_titles)

    # Add traces from the input figures to the subplot
    for i, fig in enumerate(figures):
        for trace in fig.data:
            trace.showlegend = False
            trace.name = f"{str(trace_label)}"
            trace.marker.color = BAR_COLOR
            subplot_fig.add_trace(trace, row=1, col=i + 1)

        # Add x-axis titles for all subplots
    for i in range(1, num_figs + 1):
        subplot_fig.update_xaxes(title_text=x_axes_label, row=1, col=i)

    # Update the size of subplot titles
    for i, title in enumerate(figure_titles):
        subplot_fig['layout']['annotations'][i]['font'] = dict(size=9)

    subplot_fig.update_layout(
        title_text=subplot_title,
        title_x=0.5,
        font=dict(size=10),
        yaxis_title=f"{trace_label}",
        plot_bgcolor=PLOT_BACKGROUND_COLOR,  # Change the plot background color
        margin=dict(l=20, r=20, t=80, b=80)  # Change the margins to adjust subplot background color
    )

    return subplot_fig
