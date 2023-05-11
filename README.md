# Deferral-Visualizations

This GitHub repository entails the source code and files developed for the evaluation and analysis of the Deferral solution which is part of the Master's Thesis of Tobias Boner at the
University of Zurich in 2022/2023.

The [Deferral](https://github.com/dydent/Deferral) main repository contains all other source files and code concerning the solution of the thesis.

In the following this 
Therein, this repository contains a Python project that requires a virtual environment to manage its dependencies.

## Installation Guidelines and Setup

Follow the instructions below to set up a virtual environment and install the required dependencies.

### Prerequisites

- Python 3.x
- pip (included with Python 3.4 and later)

### Setting up a virtual environment

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

### Installing dependencies

With the virtual environment activated, run the following command to install the required packages from
the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### Running the scripts

Once you've set up the virtual environment and installed the dependencies, you can run the Python scripts in the
project.

For example, if there's a script called main.py in the project, you can run it using the following command:

```
python main.py
```

Replace main.py with the name of the script you want to run.


## Results
