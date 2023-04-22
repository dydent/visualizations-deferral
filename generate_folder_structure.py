from helpers.folder_structure_generators import read_gitignore_files, print_folder_structure

gitignore_paths = ["../gitignore", "./gitignore"]
git_ignore_file_lists = read_gitignore_files(gitignore_paths)

DEFERRAL_REPO_PATH = "../"
VIS_REPO_PATH = "."

deferral_repo_ignored_folders = [".idea", "node_modules", ".git", "artifacts", "cache", "coverage", "typechain-types",
                                 ".openzeppelin", ".github", "visualizations-deferral"]

visualizations_repo_ignored_folders = ["vis-env"]

print_folder_structure(DEFERRAL_REPO_PATH, ignore_folders=deferral_repo_ignored_folders, folders_only=True,
                       markdown=True)

# print_folder_structure(VIS_REPO_PATH, ignore_folders=visualizations_repo_ignored_folders, folders_only=True, markdown=True)
