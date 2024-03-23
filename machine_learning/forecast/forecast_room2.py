import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from io import StringIO

# Load room data
room_data = pd.read_csv("room_data.csv", delimiter=";")
room_data["Timestamp"] = pd.to_datetime(room_data["Timezone : Europe/Oslo"])

# Exclude non-numeric columns from aggregation
numeric_columns = ["Temperature", "Humidity", "CO2", "Noise", "Pressure"]
room_data_numeric = room_data[["Timestamp"] + numeric_columns]

# Aggregate room data to hourly averages and convert to appropriate data type
room_data_hourly = room_data_numeric.resample('H', on='Timestamp').mean().astype(float)

# Load forecast data for future timestamps
forecast_data = pd.read_csv("weather_forecast.csv", delimiter=",", skiprows=1, names=["Timestamp", "Temperature_Forecast"])
forecast_data["Timestamp"] = pd.to_datetime(forecast_data["Timestamp"], format="%Y-%m-%d %H:%M:%S")

# Merge the datasets on timestamp using a left join
merged_data = pd.merge(room_data_hourly, forecast_data, on="Timestamp", how="left")

# Select the last 6 hours of data for training and prediction
last_6_hours_data = merged_data.tail(6)

# Feature selection: Use only the last 6 hours and 24-hour forecast value
features = last_6_hours_data[["Temperature_Forecast"]]

# Train the linear regression model for each variable
models = {}
for variable in numeric_columns:
    model = LinearRegression()
    model.fit(features, last_6_hours_data[variable])
    models[variable] = model

# Make predictions for future timestamps using the 24-hour forecast value
future_timestamps = pd.date_range(start=last_6_hours_data["Timestamp"].max(), periods=24, freq='H')  # Assuming 24 hours into the future
future_data = pd.DataFrame(index=future_timestamps, columns=["Temperature_Forecast"])
future_data["Temperature_Forecast"] = features["Temperature_Forecast"].iloc[-1]  # Use the last available forecast value

# Display or use the predictions for future timestamps
print("Predictions for Future Timestamps:")
for variable in numeric_columns:
    future_data[f"Predicted_{variable}"] = models[variable].predict(future_data[["Temperature_Forecast"]])
    print(future_data[[f"Predicted_{variable}"]])

# Plotting predicted values vs real values for each variable
for variable in numeric_columns:
    plt.figure(figsize=(10, 6))
    plt.plot(merged_data["Timestamp"], merged_data[variable], label="Real Values", color='blue')
    plt.plot(last_6_hours_data["Timestamp"], last_6_hours_data[variable], label="Last 6 Hours", color='orange', linestyle='--')
    plt.plot(future_data.index, future_data[f"Predicted_{variable}"], label="Future Predictions", color='green', linestyle='--')
    plt.xlabel("Timestamp")
    plt.ylabel(variable)
    plt.title(f"{variable} - Real vs Predicted Values")
    plt.legend()
    plt.show()
