import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
import time


# Load room data
room_data = pd.read_csv("room_data.csv", delimiter=";")
room_data["Timestamp"] = pd.to_datetime(room_data["Timezone : Europe/Oslo"])
room_data.set_index("Timestamp", inplace=True)

# Load weather forecast data
forecast_data = pd.read_csv("weather_forecast.csv")
forecast_data["Timestamp"] = pd.to_datetime(forecast_data["Timestamp"])
forecast_data.set_index("Timestamp", inplace=True)

# Exclude non-numeric columns from aggregation
numeric_columns = ["Temperature", "Humidity", "CO2", "Noise", "Pressure"]
room_data_hourly = room_data[numeric_columns].resample('H').mean()

# Align timestamps
room_data_hourly = room_data_hourly.reindex(forecast_data.index, method='nearest')

# Now merge; since they are aligned, this should not introduce any NaNs due to misalignment
merged_data = pd.merge(room_data_hourly, forecast_data, left_index=True, right_index=True)

# Handle missing values as per your chosen strategy
merged_data.dropna(inplace=True) 

# Set datasets and reset methodology_data after each type has been set
methodology_data = merged_data
m_data_2h = methodology_data.resample('2H').mean()
methodology_data = merged_data
m_data_6h = methodology_data.resample('6H').mean()
methodology_data = merged_data
m_data_24h = methodology_data.resample('24H').mean()
methodology_data = merged_data
m_data_2p = methodology_data.shift(2)
methodology_data = merged_data
m_data_6p = methodology_data.shift(6)
methodology_data = merged_data
m_data_24p = methodology_data.shift(24)
methodology_data = merged_data
# Define algorithms and methodologies
algorithms = {
    "LR": LinearRegression(),
    "SVR": SVR(),
    "GPR": GaussianProcessRegressor()#(kernel=C(1.0, (1e-3, 1e5)) * RBF(10, (1e-2, 1e2)), optimizer='fmin_l_bfgs_b')
}

methodologies = {
    "All Data": methodology_data,
    "Resampled Data": {
        "2 hours": m_data_2h,
        "6 hours": m_data_6h,
        "24 hours": m_data_24h
    },
    "Previous Data Points": {
        "2 datapoints": m_data_2p,
        "6 datapoints": m_data_6p,
        "24 datapoints": m_data_24p
    }
}

# Train models and make predictions
for algorithm_name, algorithm in algorithms.items():
    for methodology_name, methodology in methodologies.items():
        if isinstance(methodology, pd.DataFrame):
            # Training for Temperature using Temperature_Forecast
            if 'Temperature_Forecast' in methodology.columns:
                start_time = time.time()
                features = methodology[['Temperature_Forecast']].dropna()
                target = methodology['Temperature']
                model = algorithm.fit(features, target)
                predictions = model.predict(features)
                mse = ((predictions - target) ** 2).mean()
                mape = mean_absolute_error(target, predictions) / target.abs().mean() * 100
                end_time = time.time() 
                print(f"{algorithm_name} - {methodology_name} (all data) - Temperature: MSE={str(mse)[:5]}, MAPE={str(mape)[:5]}%")
                print(f"Runtime:  {end_time-start_time}")
            # Training for other variables using their historical values
            for variable in numeric_columns[1:]:
                start_time = time.time()
                features = methodology[[col for col in numeric_columns if col != variable]]
                target = methodology[variable]
                model = algorithm.fit(features, target)
                predictions = model.predict(features)
                mse = ((predictions - target) ** 2).mean()
                mape = mean_absolute_error(target, predictions) / target.abs().mean() * 100
                end_time = time.time() 
                print(f"{algorithm_name} - {methodology_name} (all data) - {variable}: MSE={str(mse)[:5]}, MAPE={str(mape)[:5]}%")
                print(f"Runtime:  {end_time-start_time}")
        else:
            for resample_name, resample_methodology in methodology.items():
                # Training for Temperature using Temperature_Forecast
                if 'Temperature_Forecast' in resample_methodology.columns:
                    start_time = time.time()
                    features = resample_methodology[['Temperature_Forecast']].dropna()                    
                    target = resample_methodology['Temperature'].dropna()
                    model = algorithm.fit(features, target)
                    predictions = model.predict(features)
                    mse = ((predictions - target) ** 2).mean()
                    mape = mean_absolute_error(target, predictions) / target.abs().mean() * 100
                    end_time = time.time()
                    print(f"{algorithm_name} - {methodology_name} {resample_name} - Temperature: MSE={str(mse)[:5]}, MAPE={str(mape)[:5]}%")
                    print(f"Runtime:  {end_time-start_time}")
                for variable in numeric_columns[1:]:
                    start_time = time.time()
                    features = resample_methodology[[col for col in numeric_columns if col != variable]]
                    target = resample_methodology[variable]
                    target = target.dropna()
                    features = features.dropna()
                    model = algorithm.fit(features, target)
                    predictions = model.predict(features)
                    mse = ((predictions - target) ** 2).mean()
                    mape = mean_absolute_error(target, predictions) / target.abs().mean() * 100
                    end_time = time.time()
                    print(f"{algorithm_name} - {methodology_name} ({resample_name}) - ({variable}): MSE={str(mse)[:5]}, MAPE={str(mape)[:5]}%")
                    print(f"Runtime:  {end_time-start_time}")

# Concatenate all dataframes from methodologies into one for plotting
all_predictions = pd.concat([methodology if isinstance(methodology, pd.DataFrame) else pd.concat(list(methodology.values())) for methodology in methodologies.values()])
all_predictions.to_csv("all_predictions.csv")