import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.gaussian_process import GaussianProcessRegressor
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
import time

# Function to generate rolling window features
def generate_rolling_features(data, window_size, numeric_columns):
    rolled_features = data[numeric_columns].rolling(window=window_size, min_periods=window_size)
    features = rolled_features.mean().dropna()  # Using mean of windows as features
    targets = data[numeric_columns].iloc[window_size:].set_index(features.index)  # Align targets with features
    return features, targets

# Load and preprocess data
def load_and_preprocess_data():
    room_data = pd.read_csv("room_data.csv", delimiter=";")
    room_data["Timestamp"] = pd.to_datetime(room_data["Timestamp"])
    room_data.set_index("Timestamp", inplace=True)

    forecast_data = pd.read_csv("weather_forecast.csv")
    forecast_data["Timestamp"] = pd.to_datetime(forecast_data["Timestamp"])
    forecast_data.set_index("Timestamp", inplace=True)

    room_data_hourly = room_data.resample('H').mean()
    room_data_hourly = room_data_hourly.reindex(forecast_data.index, method='nearest')
    merged_data = pd.merge(room_data_hourly, forecast_data, left_index=True, right_index=True)
    merged_data.dropna(inplace=True)

    return merged_data, ["Temperature", "Humidity", "CO2", "Noise", "Pressure"]

merged_data, numeric_columns = load_and_preprocess_data()

# Define algorithms
algorithms = {
    "LR": LinearRegression(),
    "SVR": SVR(),
    "GPR": GaussianProcessRegressor()
}

# Define methodologies
methodologies = {
    "All Data": merged_data,
    "Resampled Data": {
        "2 hours": merged_data.resample('2H').mean(),
        "6 hours": merged_data.resample('6H').mean(),
        "24 hours": merged_data.resample('24H').mean()
    },
    "Previous Data Points": {
        "2 datapoints": 2,
        "6 datapoints": 6,
        "24 datapoints": 24
    }
}

# Training and prediction
for algorithm_name, algorithm in algorithms.items():
    for methodology_name, methodology in methodologies.items():
        if isinstance(methodology, dict):
            # Handling resampled data or previous data points methodologies
            for resample_name, resample_data in methodology.items():
                for variable in numeric_columns:
                    if variable == "Temperature" and 'Temperature_Forecast' in resample_data.columns:
                        # Special case for temperature using forecast data directly
                        features = resample_data[['Temperature_Forecast']]
                        target = resample_data['Temperature']
                    else:
                        # Use rolling window features for other variables
                        features, targets = generate_rolling_features(resample_data, methodologies["Previous Data Points"][resample_name], numeric_columns)
                        target = targets[variable]
                    
                    if not features.empty and not target.empty:
                        model = algorithm.fit(features, target)
                        predictions = model.predict(features)
                        mse = ((predictions - target) ** 2).mean()
                        mape = mean_absolute_error(target, predictions) / target.abs().mean() * 100
                        print(f"{algorithm_name} - {resample_name} - {variable}: MSE={mse:.5f}, MAPE={mape:.5f}%")
        else:
            # Handling "All Data" methodology
            for variable in numeric_columns:
                if variable == "Temperature" and 'Temperature_Forecast' in methodology.columns:
                    # Use temperature forecast directly for temperature
                    features = methodology[['Temperature_Forecast']]
                    target = methodology['Temperature']
                else:
                    features = methodology[[col for col in numeric_columns if col != variable]]
                    target = methodology[variable]
                
                model = algorithm.fit(features, target)
                predictions = model.predict(features)
                mse = ((predictions - target) ** 2).mean()
                mape = mean_absolute_error(target, predictions) / target.abs().mean() * 100
                print(f"{algorithm_name} - All Data - {variable}: MSE={mse:.5f}, MAPE={mape:.5f}%")
