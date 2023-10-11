# Data Directory

This directory, named `data`, is dedicated to storing the raw data collected during the Arduino Sensor Experiment. Currently, it houses the `datalog.csv` file, which contains crucial data points from the experiment.

## Files in this Directory

### 1. datalog.csv

#### Description:
The `datalog.csv` is a CSV (Comma-Separated Values) file that holds the readings from the Arduino Sensor Experiment. Each row represents a unique reading, and the columns are structured as follows:

- **ReadingID**: A unique identifier for each reading.
- **Timestamp**: A timestamp indicating when the reading was taken.
- **SensorID**: An identifier for the sensor that took the reading.
- **RawReading**: The raw data value obtained from the sensor.
- **CalculatedHumidity**: The humidity value calculated from the raw reading.
- **Error**: The calculated error between the true humidity and the value obtained from the sensor.

#### Usage:
You can view the `datalog.csv` using any CSV viewer or text editor. Tools like Microsoft Excel, LibreOffice Calc, or even plain text editors can open and display the contents.

For more detailed analysis or to process this data, refer to the scripts available in the `process_raw_data` directory.

