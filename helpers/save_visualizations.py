import os
from plotly.graph_objs import Figure
# local imports
from helpers.constants.result_path_constants import VISUALIZATION_RESULT_PATH


def save_visualization_figure(fig: Figure, file_name: str, base_folder: str, file_folder: str = "") -> None:
    # Create the folder if it doesn't exist
    result_folder = f'../../{VISUALIZATION_RESULT_PATH}/' + base_folder + '/' + file_folder
    os.makedirs(result_folder, exist_ok=True)

    # Save the figure as an image
    file_path = os.path.join(result_folder, f"{file_name}.png")
    fig.write_image(file_path)
