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



forecast_data = pd.read_csv("weather_forecast.csv", delimiter=",", skiprows=1, names=["Timestamp", "Temperature_Forecast"])
forecast_data["Timestamp"] = pd.to_datetime(forecast_data["Timestamp"], format="%Y-%m-%d %H:%M:%S")
print(forecast_data)



# Merge the datasets on timestamp using a left join
merged_data = pd.merge(room_data_hourly, forecast_data, on="Timestamp", how="left")

# Drop rows with missing values in forecast columns
merged_data = merged_data.dropna(subset=["Temperature_Forecast"])

# Feature selection
features = merged_data[["Temperature_Forecast"]]

# Target variables
target_variables = merged_data[numeric_columns]

# Drop rows with missing values in target variables
merged_data = merged_data.dropna(subset=numeric_columns)

# Train the linear regression model for each variable
models = {}
for variable in target_variables.columns:
    model = LinearRegression()
    model.fit(features, target_variables[variable])
    models[variable] = model

# Make predictions for all data
predictions = pd.DataFrame({variable: models[variable].predict(features) for variable in target_variables.columns})

# Evaluate the model (you might want to use a different evaluation metric for multi-variable predictions)
mse = ((predictions - target_variables) ** 2).mean()
print(f"Mean Squared Error: {mse}")

# Save the predictions to a new file
for variable in target_variables.columns:
    merged_data[f"Predicted_{variable}"] = models[variable].predict(features)

merged_data.to_csv("room_variable_predictions_all_data.csv", index=False)

# Plotting predicted values vs real values for each variable
for variable in target_variables.columns:
    plt.figure(figsize=(10, 6))
    plt.plot(merged_data["Timestamp"], merged_data[variable], label="Real Values", color='blue')
    plt.plot(merged_data["Timestamp"], merged_data[f"Predicted_{variable}"], label="Predicted Values", color='red')
    plt.xlabel("Timestamp")
    plt.ylabel(variable)
    plt.title(f"{variable} - Real vs Predicted Values")
    plt.legend()
    plt.show()


''''''