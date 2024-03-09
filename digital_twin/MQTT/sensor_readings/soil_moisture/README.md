# Arduino Sensor Experiment
This folder contains the files and scripts related to the Arduino Sensor Experiment.

## Install Requirements
Before running the scripts, you need to install the required Python packages. You can do this by running:
pip install -r requirements.txt


## Programs

### Data Collection
This folder contains data collected directly from the Arduino in the form of a CSV file (`datalog.csv`). This CSV holds readings such as timestamps, sensor IDs, raw readings, calculated humidity, and error values.

### Error Calculation Script
I have a script named `calculate_error.py` that allows users to input the true humidity readings for specific sensors on a given day. It then calculates the error between the true value and the readings in the CSV and updates the CSV with these error values.

Usage:
Navigate into the directory where the script is located, then run this script:
python calculate_error.py


### Error Visualization Script
There's also a script named `graph_error.py` that generates a graphical view of the errors for each day on each sensor. This visual representation helps in quickly grasping the deviation trends of the sensors over time.

Usage:
Navigate into the directory where the script is located, then run this script:
python graph_error.py


