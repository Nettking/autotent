import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX

# Load room data
room_data = pd.read_csv("room_data.csv", delimiter=";")
room_data["Timestamp"] = pd.to_datetime(room_data["Timezone : Europe/Oslo"])

# Exclude non-numeric columns from aggregation
numeric_columns = ["Temperature", "Humidity", "CO2", "Noise", "Pressure"]
room_data_numeric = room_data[["Timestamp"] + numeric_columns]

# Aggregate room data to hourly averages and convert to an appropriate data type
room_data_hourly = room_data_numeric.resample('H', on='Timestamp').mean().astype(float)

# Load weather forecast data
forecast_data = pd.read_csv("weather_forecast.csv", delimiter=",", skiprows=1, names=["Timestamp", "Temperature_Forecast"])
forecast_data["Timestamp"] = pd.to_datetime(forecast_data["Timestamp"], format="%Y-%m-%d %H:%M:%S")

# Merge the datasets on timestamp using a left join
merged_data = pd.merge(room_data_hourly, forecast_data, on="Timestamp", how="left")

# Drop rows with missing values in forecast columns
merged_data = merged_data.dropna(subset=["Temperature_Forecast"])

# Feature selection
features = merged_data[["Temperature_Forecast"]]

# Target variable
target_variable = merged_data["Temperature"]

# Train the SARIMA model
order = (1, 1, 1)  # Order parameters (p, d, q)
seasonal_order = (1, 1, 1, 24)  # Seasonal order parameters (P, D, Q, s)

sarima_model = SARIMAX(target_variable, order=order, seasonal_order=seasonal_order)
sarima_results = sarima_model.fit()

# Make predictions for all data
predictions = sarima_results.get_forecast(steps=len(merged_data))
predicted_values = predictions.predicted_mean

# Evaluate the model
mse = ((predicted_values - target_variable) ** 2).mean()
print(f"Mean Squared Error (SARIMA): {mse}")

# Save the predictions to a new file
merged_data["Predicted_Temperature_SARIMA"] = predicted_values
merged_data.to_csv("room_variable_predictions_all_data_sarima.csv", index=False)

# Plotting predicted values vs real values for temperature
plt.figure(figsize=(10, 6))
plt.plot(merged_data["Timestamp"], target_variable, label="Real Values", color='blue')
plt.plot(merged_data["Timestamp"], predicted_values, label="Predicted Values (SARIMA)", color='red')
plt.xlabel("Timestamp")
plt.ylabel("Temperature")
plt.title("Temperature - Real vs Predicted Values (SARIMA)")
plt.legend()
plt.show()
