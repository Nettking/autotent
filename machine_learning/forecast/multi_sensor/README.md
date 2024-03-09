# Environmental Data Visualization
This Python script allows you to visualize environmental data from a CSV file. It reads data from a CSV file with a specific structure and generates line graphs for selected data fields over time.

## Requirements

Before using this script, make sure you have the following libraries installed:

- [pandas](https://pandas.pydata.org/)
- [matplotlib](https://matplotlib.org/)

You can install them using pip:

```bash
pip install pandas matplotlib
```	
The script will display a menu of available data to plot:
### Available data to plot:
1. Temperature (°C)
2. Humidity (%)
3. CO2 (ppm)
4. Noise
5. Pressure (hPa)

Enter the number corresponding to the data you want to plot and press Enter.

The script will generate a line graph showing the selected data field over time.