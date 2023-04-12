import os
from plotly.graph_objs import Figure


def save_visualization_figure(fig: Figure, file_name: str, folder: str = "results") -> None:
    # Create the folder if it doesn't exist
    os.makedirs(folder, exist_ok=True)

    # Save the figure as an image
    file_path = os.path.join(folder, f"{file_name}.png")
    fig.write_image(file_path)
