# ---------------------------------------------------------------------------------
# helper functions to create overall metric tables
# ---------------------------------------------------------------------------------

def numprint_formatter(x, rounded_decimal: int = 3):
    # Check if the input is a number (int or float)
    if isinstance(x, (int, float)):
        # Round the number to 3 decimal places
        rounded_x = round(x, rounded_decimal)
        # Return the rounded number formatted as a LaTeX \numprint command
        return r'\numprint{%s}' % rounded_x
    return x


def generate_overall_latex_table(data_array, metric_keys, metric_type: str, tabel_caption: str = "Your Caption",
                                 table_label: str = "tab:table_label", rounded_decimal: int = 3):
    # Begin LaTeX table header, setting the columns and top rule
    latex_table = (
            "%===============================================================================\n"
            "\\begin{sidewaystable}[]\n"
            "\\centering\n"
            "{\\small\n"
            "\\begin{tabular}{l" + "c" * len(metric_keys) + "}\n"
                                                            "\\toprule\n"
                                                            "Deferral Contract & " + " & ".join(
        [f"{key}" for key in metric_keys]) + "\\\\\n"
                                             "\\midrule\n"
    )

    # Iterate over the data array, extracting the contract name and metric values
    for data in data_array:
        contract_name = data["contractName"]
        # Format the metric values with the numprint_formatter function
        formatted_values = [
            numprint_formatter(float(data["metrics"][key][metric_type]), rounded_decimal=rounded_decimal) for key in
            metric_keys]
        # Add a row for the current contract and its metric values to the LaTeX table
        latex_table += f"{contract_name} & " + " & ".join(formatted_values) + "\\\\\n"

    # End LaTeX table, adding the bottom rule, caption, and label
    latex_table += (
        "\\bottomrule\n"
        "\\end{tabular}\n"
        "} % Close the \\small command here\n"
        f"\\caption{{{tabel_caption}}}\n"  # Replace 'Your Caption' with the desired caption
        f"\\label{{{table_label}}}\n"  # Replace 'your_label' with the desired label
        "\\end{sidewaystable}\n"
        "%===============================================================================\n"
    )

    return latex_table
