# Strawberry Berry Production Analysis
## Overview
This Python script is designed to analyze and visualize strawberry berry production data, focusing on size (height, width, diameter) and weight over time. It reads data from a CSV file, calculates average sizes and weights, and generates plots to visualize the data trends.

### Prerequisites
Before running the script, make sure you have the following installed:

Python (3.x recommended)
Pandas library
Matplotlib library

You can install Pandas and Matplotlib using pip:
```bash
pip install pandas matplotlib
```
### Usage
Place your strawberry berry production data in a CSV file named "data.csv" or specify the path to your data file in the data_path variable.

Run the script using the following command:

```bash
python strawberry_production_analysis.py
```

This will read the data, calculate average sizes and weights, and generate plots.

### Script Breakdown
The script reads data from the CSV file specified in the data_path variable.

It defines a function calculate_average_sizes_and_weights(dataframe) that calculates and prints the average height, width, diameter, and weight of the strawberries.

The script converts the "Date" column to datetime format for better date handling.

#### It generates two subplots:

- Strawberry size (height, width, diameter) over time.
- Strawberry weight over time.
- The script then displays the plots and prints the average sizes and weights.

### Customization
You can customize the script by replacing the data in the CSV file with your own strawberry production data. Adjust the data file path if it's located in a different directory.

#### Dependencies
Pandas: Used for data manipulation and analysis.
Matplotlib: Used for creating data visualizations.