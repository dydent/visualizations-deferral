import os
from helpers.constants.result_path_constants import VISUALIZATION_RESULT_PATH


def save_table(table_output: str, file_name: str, base_folder: str, file_folder: str = "") -> None:
    # Create the folder if it doesn't exist
    result_folder = f'{VISUALIZATION_RESULT_PATH}/' + base_folder + '/' + file_folder
    os.makedirs(result_folder, exist_ok=True)

    # Save the figure as an image
    file_path = os.path.join(result_folder, f"{file_name}.txt")

    # Check if the target file already exists, and if it does, replace it with the new file
    if os.path.exists(file_path):
        print(f"File already exists at {file_path}. Overwriting the file.")
        os.remove(file_path)

    with open(file_path, "w") as file:
        file.write(table_output)

    print(f"Table saved to {file_path}")
