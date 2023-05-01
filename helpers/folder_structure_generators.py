import os


# ---------------------------------------------------------------------------------
# helper functions to print folder structure of a folder
# ---------------------------------------------------------------------------------


def read_gitignore_files(file_paths):
    # Initialize an empty list to store the folder names to ignore
    gitignore_folders = []

    # Iterate through each file path in the provided list
    for file_path in file_paths:
        # Check if the file exists at the given file path
        if os.path.exists(file_path):
            # Open the file and read its content
            with open(file_path, "r") as file:
                gitignore_content = file.readlines()

            # Extract non-empty, non-comment lines from the content and add them to the ignore list
            gitignore_folders += [line.strip() for line in gitignore_content if
                                  line.strip() and not line.startswith("#")]

    # Return the list of folder names to ignore
    return gitignore_folders


def print_folder_structure(start_path, ignore_folders=None, folders_only=False, depth=0, markdown=False, latex=False):
    if ignore_folders is None:
        ignore_folders = []

    if depth == 0 and latex:
        print("\\dirtree{%")

    for item in sorted(os.listdir(start_path)):
        if item in ignore_folders:
            continue

        item_path = os.path.join(start_path, item)

        if os.path.isdir(item_path):
            if latex:
                print(f"{'.%d' % (depth + 1)} {item}/.")
            elif markdown:
                print(f"{'  ' * depth}- {item}/")
            else:
                print("|  " * depth + "|-- " + item)
            print_folder_structure(item_path, ignore_folders, folders_only, depth + 1, markdown, latex)
        elif not folders_only:
            if latex:
                print(f"{'.%d' % (depth + 1)} {item}.")
            elif markdown:
                print(f"{'  ' * depth}- {item}")
            else:
                print("|  " * depth + "|-- " + item)

    if depth == 0 and latex:
        print("}")
