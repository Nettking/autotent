import pandas as pd
from sklearn.svm import SVR
import matplotlib.pyplot as plt

# Load room data
room_data = pd.read_csv("room_data.csv", delimiter=";")
room_data["Timestamp"] = pd.to_datetime(room_data["Timezone : Europe/Oslo"])

# Exclude non-numeric columns from aggregation
numeric_columns = ["Temperature", "Humidity", "CO2", "Noise", "Pressure"]
room_data_numeric = room_data[["Timestamp"] + numeric_columns]

# Aggregate room data to different time windows (2 hours, 6 hours, and 24 hours) and convert to appropriate data type
resample_freqs = ['2H', '6H', '24H']
room_data_resampled = {freq: room_data_numeric.resample(freq, on='Timestamp').mean().astype(float) for freq in resample_freqs}

forecast_data = pd.read_csv("weather_forecast.csv", delimiter=",", skiprows=1, names=["Timestamp", "Temperature_Forecast"])
forecast_data["Timestamp"] = pd.to_datetime(forecast_data["Timestamp"], format="%Y-%m-%d %H:%M:%S")

# Merge the datasets on timestamp using a left join
merged_data = {}
for freq, resampled_data in room_data_resampled.items():
    merged_data[freq] = pd.merge(resampled_data, forecast_data, on="Timestamp", how="left")

    # Drop rows with missing values in forecast columns
    merged_data[freq] = merged_data[freq].dropna(subset=["Temperature_Forecast"])

    # Feature selection
    features = merged_data[freq][["Temperature_Forecast"]]

    # Target variables
    target_variables = merged_data[freq][numeric_columns]

    # Drop rows with missing values in target variables
    merged_data[freq] = merged_data[freq].dropna(subset=numeric_columns)

    # Train the SVR model for each variable
    models = {}
    for variable in target_variables.columns:
        model = SVR(kernel='rbf')  # You can choose different kernels as per your requirement

        # Select last six readings for training
        features_train = features[-6:]
        target_train = target_variables[variable][-6:]

        model.fit(features_train, target_train)
        models[variable] = model

    # Make predictions for all data
    predictions = pd.DataFrame({variable: models[variable].predict(features) for variable in target_variables.columns})

    # Evaluate the model (you might want to use a different evaluation metric for multi-variable predictions)
    mse = ((predictions - target_variables) ** 2).mean()
    print(f"Mean Squared Error ({freq}): {mse}")

    # Save the predictions to a new file
    for variable in target_variables.columns:
        merged_data[freq][f"Predicted_{variable}"] = models[variable].predict(features)

        # Plotting predicted values vs real values for each variable
        plt.figure(figsize=(10, 6))
        plt.plot(merged_data[freq]["Timestamp"], merged_data[freq][variable], label="Real Values", color='blue')
        plt.plot(merged_data[freq]["Timestamp"], merged_data[freq][f"Predicted_{variable}"], label="Predicted Values", color='red')
        plt.xlabel("Timestamp")
        plt.ylabel(variable)
        plt.title(f"{variable} - Real vs Predicted Values ({freq})")
        plt.legend()
        plt.show()

    # Save the predictions to a new file
    merged_data[freq].to_csv(f"room_variable_predictions_{freq}.csv", index=False)
