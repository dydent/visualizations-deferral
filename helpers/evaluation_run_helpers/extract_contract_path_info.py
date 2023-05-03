# ---------------------------------------------------------------------------------
# helper functions to get evaluation file and contract infos
# ---------------------------------------------------------------------------------


def extract_contract_path_info(file_names):
    info_dict = {}
    for file_name in file_names:
        # Extract the path value and contract name from the file name
        path_value = file_name.split('/')[-3]
        contract_name = file_name.split('/')[-1].split('-')[0]

        # Add the path value, contract name, and full path to the dictionary
        if path_value not in info_dict:
            info_dict[path_value] = []
        info_dict[path_value].append({'contract_name': contract_name, 'full_path': file_name})

    return info_dict
