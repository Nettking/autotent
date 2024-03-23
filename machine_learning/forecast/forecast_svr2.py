import pandas as pd
from sklearn.svm import SVR
import matplotlib.pyplot as plt


# Load room data
room_data = pd.read_csv("room_data.csv", delimiter=";")
room_data["Timestamp"] = pd.to_datetime(room_data["Timezone : Europe/Oslo"])


# Exclude non-numeric columns from aggregation
numeric_columns = ["Temperature", "Humidity", "CO2", "Noise", "Pressure"]
room_data_numeric = room_data[["Timestamp"] + numeric_columns]


forecast_data = pd.read_csv("weather_forecast.csv", delimiter=",", skiprows=1, names=["Timestamp", "Temperature_Forecast"])
forecast_data["Timestamp"] = pd.to_datetime(forecast_data["Timestamp"], format="%Y-%m-%d %H:%M:%S")


# Define a function to extract features from the last n hours
def extract_features_last_n_hours(data, n_hours):
    # Filter data for the last n hours
    last_n_hours_data = data[data['Timestamp'] >= data['Timestamp'].max() - pd.Timedelta(hours=n_hours)]
    # Return only numeric values
    return last_n_hours_data.drop(columns=["Timestamp"])


# Merge the datasets on timestamp using a left join
merged_data = pd.merge(room_data_numeric, forecast_data, on="Timestamp", how="left")

# Drop rows with missing values in forecast columns
merged_data = merged_data.dropna(subset=["Temperature_Forecast"])

# Target variables
target_variables = merged_data[numeric_columns]

# Drop rows with missing values in target variables
merged_data = merged_data.dropna(subset=numeric_columns)

# Define time windows
time_windows = [2, 4, 6, 24]

# Train SVR model for each time window
models = {}
for window in time_windows:
    # Extract features for the time window
    features = extract_features_last_n_hours(merged_data, window)

    # Train the SVR model for each variable
    models[window] = {}
    for variable in target_variables.columns:
        model = SVR(kernel='rbf')  # You can choose different kernels as per your requirement
        model.fit(features, target_variables[variable])
        models[window][variable] = model

        # Make predictions for all data
        predictions = model.predict(features)

        # Evaluate the model (you might want to use a different evaluation metric for multi-variable predictions)
        mse = ((predictions - target_variables[variable]) ** 2).mean()
        print(f"Mean Squared Error ({window} hours, {variable}): {mse}")

        # Save the predictions to a new file
        merged_data[f"Predicted_{variable}_{window}h"] = predictions

# Save the predictions to a new file
merged_data.to_csv("room_variable_predictions_all_data.csv", index=False)
