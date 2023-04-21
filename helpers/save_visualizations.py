import os
from plotly.graph_objs import Figure


def save_visualization_figure(fig: Figure, file_name: str, base_folder: str, file_folder: str = "") -> None:
    # Create the folder if it doesn't exist
    result_folder = '../../result-visualization-files/' + base_folder + '/' + file_folder
    os.makedirs(result_folder, exist_ok=True)

    # Save the figure as an image
    file_path = os.path.join(result_folder, f"{file_name}.png")
    fig.write_image(file_path)
