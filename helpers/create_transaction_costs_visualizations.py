def create_transactions_costs_visualizations(df: pd.DataFrame, x_axis: str, y_axis: str, title: str, x_axis_title: str,
                                             y_axis_title: str,
                                             html_output: bool = False):
    # create chart
    if x_axis == 'index' or x_axis == 'txIndex':
        fig = px.bar(df, y=df[y_axis], hover_data=df.columns)
    else:
        fig = px.bar(df, x=df[x_axis], y=df[y_axis], color=df[y_axis], hover_data=df.columns)

    # configure layout
    fig.update_layout(
        title=str.title(title),
        title_x=0.5,  # Center the title
        font=dict(size=8),
        xaxis_title=str.title(x_axis_title),
        yaxis_title=str.title(y_axis_title))

    # show and output chart
    if html_output:
        fig.write_html('{}.html'.format(title), auto_open=True)
        fig.show()
    #  return plot
    return fig
