from helpers.converters.convert_string_to_number import convert_string_to_number


# ---------------------------------------------------------------------------------
# helper functions to extract baseline gas used values
# ---------------------------------------------------------------------------------


def extract_baseline_gas_used_values(data_array, parameter='avg'):
    baseline_dict = {}
    for item in data_array:
        contract_name = item['contractName']
        try:
            value = item['metrics']['gasUsed'][parameter]
            users = item['numberOfUsers']
        except KeyError as e:
            print(f"{e} not found for {contract_name}. Skipping this item.")
            continue
        if contract_name not in baseline_dict:
            baseline_dict[contract_name] = {
                'gas_used_metric_name': f'{parameter}GasUsed-{users}-users',
                'gas_used_baseline_value': convert_string_to_number(value),
            }
    return baseline_dict
