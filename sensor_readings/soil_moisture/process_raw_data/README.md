# Process Raw Data

This directory, `process_raw_data`, contains scripts that allow users to process and analyze the raw data collected during the Arduino Sensor Experiment. The primary focus is on calculating errors and visually representing these errors through graphs.

## Scripts in this Directory

### 1. calculate_error.py

#### Description:
This script lets users input the true humidity readings for specific sensors on a selected day. It then compares the true values with the readings in the `datalog.csv` file and calculates the error. The CSV is then updated with these error values.

#### Usage:
To run the script, use the following command:
python calculate_error.py

When prompted, input the week number (between 1-5) and the day number (between 1-7). Subsequently, provide the true humidity readings for the respective sensors of the chosen day.

### 2. graph_error.py

#### Description:
This script processes the `datalog.csv` file to graphically represent the errors for each day on each sensor. The errors are plotted as absolute values, which aids in understanding the magnitude of deviation without focusing on the direction (positive or negative).

#### Usage:
To generate the graphs, run the script with:
python graph_error.py

A plot will appear showcasing the error values for each sensor on different days. Each sensor has a unique line on the graph to help differentiate between them.

## Dependencies:
Ensure that you have all the required Python packages installed. Typically, you would need `csv` (which is part of Python's standard library) and `matplotlib`. These dependencies can be installed using `pip`.
pip install -r requirements.txt