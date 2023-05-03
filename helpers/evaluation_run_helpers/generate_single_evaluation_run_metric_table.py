# ---------------------------------------------------------------------------------
# helper functions to generate evaluation run specific latex visualization tables
# ---------------------------------------------------------------------------------


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
