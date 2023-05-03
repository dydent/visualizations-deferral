def generate_latex_table_single_object(data_object, metric_keys):
    # Begin LaTeX table
    latex_table = (
        "\\begin{table}[]\n"
        "\\centering\n"
        "{\\small\n"
        "\\begin{tabular}{lccccc}\n"
        "\\toprule\n"
        "Metric & Avg & Min & Max & Median & Sum\\\\\n"
        "\\midrule\n"
    )

    # Add data to the table
    for index, metric in enumerate(metric_keys):
        avg_value = data_object["metrics"][metric]["avg"]
        min_value = data_object["metrics"][metric]["min"]
        max_value = data_object["metrics"][metric]["max"]
        median_value = data_object["metrics"][metric]["median"]
        sum_value = data_object["metrics"][metric]["sum"]

        latex_table += (
            f"{metric} & \\numprint{{{avg_value}}} & \\numprint{{{min_value}}} & "
            f"\\numprint{{{max_value}}} & \\numprint{{{median_value}}} & \\numprint{{{sum_value}}}\\\\\n"
        )

        if index < len(metric_keys) - 1:  # Add midrule if not the last row
            latex_table += "\\midrule\n"

    # End LaTeX table
    latex_table += (
        "\\bottomrule\n"
        "\\end{tabular}\n"
        "} % Close the \\small command here\n"
        "\\caption{Your Caption}\n"  # Replace 'Your Caption' with the desired caption
        "\\label{tab:your_label}\n"  # Replace 'your_label' with the desired label
        "\\end{table}\n"
    )

    return latex_table


def generate_latex_table_with_human_readable_values_v2(
        data, metrics_keys, table_caption: str = "Your Caption", table_label: str = "tab:table_label"
):
    latex_table = (
        "%===============================================================================\n"
        "\\begin{table}[]\n"
        "\\centering\n"
        "{\\small\n"
        "\\begin{tabular}{lccccc} \\toprule\n"
        "Metric & Avg & Min & Max & Median & Sum \\\\ \\midrule\n"
    )

    for key in metrics_keys:
        row = (
            f"{key} & "
            f"\\numprint{{{float(data['metrics'][key]['avg'])}}} & "
            f"\\numprint{{{float(data['metrics'][key]['min'])}}} & "
            f"\\numprint{{{float(data['metrics'][key]['max'])}}} & "
            f"\\numprint{{{float(data['metrics'][key]['median'])}}} & "
            f"\\numprint{{{float(data['metrics'][key]['sum'])}}} \\\\ \n"
        )
        latex_table += row

    latex_table += (
        "\\bottomrule\n"
        "\\end{tabular}\n"
        "} % Close the \\small command here\n"
        f"\\caption{{{table_caption}}}\n"
        f"\\label{{{table_label}}}\n"
        "\\end{table}\n"
        "%===============================================================================\n"
    )

    return latex_table


def generate_latex_table_with_human_readable_values_rounded(
        data, metrics_keys, table_caption: str = "Your Caption", table_label: str = "tab:table_label",
        round_decimals: int = 3, metric_table_caption: str = "Metrics"
):
    latex_table = (
        "%===============================================================================\n"
        f"% {table_caption}\n"
        f"% rounded to {round_decimals} decimals\n"
        "%===============================================================================\n"
        "\\begin{table}[]\n"
        "\\centering\n"
        "{\\small\n"
        "\\begin{tabular}{lccccc} \\toprule\n"
        f"{{{metric_table_caption}}} & Avg & Min & Max & Median & Sum \\\\ \\midrule\n"
    )

    for key in metrics_keys:
        row = (
            f"{key} & "
            f"\\numprint{{{round(float(data['metrics'][key]['avg']), round_decimals)}}} & "
            f"\\numprint{{{round(float(data['metrics'][key]['min']), round_decimals)}}} & "
            f"\\numprint{{{round(float(data['metrics'][key]['max']), round_decimals)}}} & "
            f"\\numprint{{{round(float(data['metrics'][key]['median']), round_decimals)}}} & "
            f"\\numprint{{{round(float(data['metrics'][key]['sum']), round_decimals)}}} \\\\ \n"
        )
        latex_table += row

    latex_table += (
        "\\bottomrule\n"
        "\\end{tabular}\n"
        "} % Close the \\small command here\n"
        f"\\caption{{{table_caption}}}\n"
        f"\\label{{{table_label}}}\n"
        "\\end{table}\n"
        "%===============================================================================\n"
    )

    return latex_table
