#!/bin/bash

directory_to_remove=$(python -c "from helpers.constants.result_path_constants import VISUALIZATION_RESULT_PATH; print(VISUALIZATION_RESULT_PATH)")
rm -rf "$directory_to_remove"
