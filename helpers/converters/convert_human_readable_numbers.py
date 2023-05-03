# ---------------------------------------------------------------------------------
# helper functions to convert numbers
# ---------------------------------------------------------------------------------


def human_readable_format(num, latex=False):
    """
    Convert a numeric value to a human-readable format with units (K, M, B, T, Q) and
    for small numbers (m, µ, n, p, f)

    Args:
        num (float): The numeric value to be converted.
        latex (bool): Set to True if the output string will be used in LaTeX. Default is False.

    Returns:
        str: The human-readable representation of the value.

    Examples:
        1000 -> 1.0K (Thousand)
        1000000 -> 1.0M (Million)
        1000000000 -> 1.0B (Billion)
        1000000000000 -> 1.0T (Trillion)
        1000000000000000 -> 1.0Q (Quadrillion)
        0.001 -> 1.0m (Milli)
        0.000001 -> 1.0µ (Micro) or 1.0\si{\micro} (LaTeX compatible)
        0.000000001 -> 1.0n (Nano)
        0.000000000001 -> 1.0p (Pico)
        0.000000000000001 -> 1.0f (Femto)
    """
    if num >= 1:
        for unit in ['', 'K', 'M', 'B', 'T']:
            if abs(num) < 1000:
                return f"{num:.1f}{unit}"
            num /= 1000
        return f"{num:.1f}Q"
    else:
        for unit in ['', 'm', ('\\si{\\micro}' if latex else 'µ'), 'n', 'p', 'f']:
            if abs(num) >= 0.001:
                return f"{num * (1000 if unit != '' else 1):.1f}{unit}"
            num *= 1000
        return f"{num:.1f}a"  # Atto
