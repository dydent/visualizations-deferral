def generate_latex_table(data_array, metric, tabel_caption: str = "Your Caption", table_label: str = "tab:table_label"):
    # Begin LaTeX table
    latex_table = (
        "%===============================================================================\n"
        "\\begin{table}[]\n"
        "\\centering\n"
        "{\\small\n"
        "\\begin{tabular}{lcccc}\n"
        "\\toprule\n"
        f"Nr. of Users & Avg {metric} & Min {metric} & Max {metric} & Median {metric}\\\\\n"
        "\\midrule\n"
    )

    # Add data to the table
    for data in data_array:
        num_users = data["numberOfUsers"]
        avg_value = data["metrics"][metric]["avg"]
        min_value = data["metrics"][metric]["min"]
        max_value = data["metrics"][metric]["max"]
        median_value = data["metrics"][metric]["median"]

        latex_table += (
            f"\\numprint{{{num_users}}} & \\numprint{{{avg_value}}} & \\numprint{{{min_value}}} & "
            f"\\numprint{{{max_value}}} & \\numprint{{{median_value}}}\\\\\n"
        )

    # End LaTeX table
    latex_table += (
        "\\bottomrule\n"
        "\\end{tabular}\n"
        "} % Close the \\small command here\n"
        f"\\caption{{{tabel_caption}}}\n"  # Replace 'Your Caption' with the desired caption
        f"\\label{{{table_label}}}\n"  # Replace 'your_label' with the desired label
        "\\end{table}\n"
        "%===============================================================================\n"
    )

    return latex_table
