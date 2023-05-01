# ---------------------------------------------------------------------------------
# helper functions to convert list values to numbers
# ---------------------------------------------------------------------------------


def convert_to_numbers(values: list):
    converted_values = []

    for value in values:
        try:
            converted_value = float(value)
        except ValueError:
            converted_value = 0

        converted_values.append(converted_value)

    return converted_values
