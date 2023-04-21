def convert_string_to_number(s: str):
    """
    Convert a string to either an int or a float, depending on the input.
    If the string cannot be converted to a number, return the original string.

    param s: The input string to be converted.
    return: The converted int or float value, or the original string if conversion is not possible.
    """
    try:
        # Attempt to convert the string to an integer
        return int(s)
    except ValueError:
        # If the conversion to integer fails, try converting to a float
        try:
            return float(s)
        except ValueError:
            # If both integer and float conversion fail, return the original string
            return s
