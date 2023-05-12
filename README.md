
# Deferral-Visualizations

This GitHub repository entails the source code and files developed for the evaluation and analysis of the Deferral solution, which is part of the Master's Thesis of Tobias Boner at the
University of Zurich in 2022/2023.

The [Deferral](https://github.com/dydent/Deferral) main repository contains all other source files and code concerning the solution of the thesis.

This repository contains Python and other scripts that are used to analyze and evaluate the results.


# Installation Guidelines and Setup

Follow the instructions below to set up a virtual environment and install the required dependencies.

### Prerequisites

- Python 3.x
- pip (included with Python 3.4 and later)

Be aware that file paths differ between Windows and Mac \& Linux due to their differing syntax.
Hence, this can lead to errors in the code and scripts when using Windows.
Therefore it is recommended to use Mac or Linux.

### Setup Submodule Repository
1. Clone this repository: 
	- ``` git clone https://github.com/dydent/visualizations-deferral ``` 

Ensure this repository is included and located in the root folder of the [Deferral main repository](https://github.com/dydent/Deferral). To set up the main repository, follow the instructions in the corresponding [README](https://github.com/dydent/Deferral/blob/main/README.md) file. 

This repository can also be located in a different folder. However, the file and folder paths used in the code must then be adjusted.

### Setup Virtual Environment

1. Open a terminal/command prompt and navigate to the project directory.
2. Run the following command to create a virtual environment:
    - For Linux and macOS:
      ```bash
      python3 -m venv myenv
      ```
    - For Windows:
      ```bash
      py -m venv myenv
      ```
   Replace `myenv` with the desired name for your virtual environment directory.
   
3. Activate the virtual environment:
    - For Linux and macOS:
      ```bash
      source myenv/bin/activate
      ```
    - For Windows:
      ```bash
      myenv\Scripts\activate.bat
      ```
   Make sure to replace `myenv` with the name of your virtual environment directory.

### Installing Dependencies

With the virtual environment activated, run the following command to install the required packages from
the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### Env Variables
It is necessary to create a local `.env` file containing key-value pairs of environment variables the project requires.

The `.env.example` file shows examples of all the values that must be set up and includes explanations for the different values.


### Running the Scripts

Once you've set up the virtual environment and installed the dependencies, you can run the Python scripts in the
project.

For example, if there's a script called main.py in the project, you can run it using the following command:

```
python script.py
```

Replace script.py with the name of the script you want to run.

Additionally, the `generate_visualization_results.sh` shell script can be run to execute all visualization scripts at once by running `.\generate_visualization_results.sh` in the terminal.


## Evaluation and Visualization Result Files

All the generated visualization and visualization result files are stored locally in the `visualization-result-files` directory.
 
The result folder structure looks like this:
- **historical**/ *contains results related to historical gas and fiat prices*
- **overall**/ *contains results for the overall view across all contracts*
- **referral-multilevel-token-rewards**/ *contains contract-specific evaluation results grouped by the contracts*
- **referral-payment-multilevel-rewards**/ *contains contract-specific evaluation results grouped by the contracts*
- **referral-payment-quantity**/ *contains contract-specific evaluation results grouped by the contracts*
- **referral-payment-transmitter**/ *contains contract-specific evaluation results grouped by the contracts*
- **referral-payment-value**/ *contains contract-specific evaluation results grouped by the contracts*

