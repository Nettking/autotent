import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
import time

plt.rcParams.update({'font.size': 14})

# Function to generate rolling window features
def generate_rolling_features(data, window_size):
    rolled_features = data[numeric_columns].rolling(window=window_size, min_periods=window_size)
    features = rolled_features.mean()#.dropna()  
    return features

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
m_data_2p = generate_rolling_features(methodology_data, 2)
methodology_data = merged_data
m_data_6p = generate_rolling_features(methodology_data, 6)
methodology_data = merged_data
m_data_24p = generate_rolling_features(methodology_data, 24)
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

def set_ylabel(variable):
    if variable == 'Temperature_Forecast':
        y_label_string = "Temperature_Forecast"
    if variable == "Noise":
        y_label_string = variable + " (dB)"
    if variable == "Humidity":
        y_label_string = variable + " (%)"
    if variable == "CO2":
        y_label_string = variable + " (PPM)"
    if variable == "Pressure":
        y_label_string = variable + " (hPa)"
    if variable == "Temperature":
        y_label_string = variable + " (°C)"
    
    return y_label_string

def plot_predicted_graph(target, variable, predictions, algorithm_name, methodology_name, resample_name):
    plt.figure(figsize=(10, 5))
    plt.plot(target.index, target, label='Ground Truth')
    plt.plot(target.index, predictions, label='Predictions', linestyle='--')
    plt.title(f"Predicting {variable} using {algorithm_name} with {methodology_name} {resample_name} ")
    plt.xlabel('Time')
    y_label = set_ylabel(variable)
    plt.ylabel(y_label)
    plt.legend()
    plt.grid(True)
    #plt.show()
    plt.savefig(f"{variable}_{algorithm_name}_{methodology_name}_{resample_name}_predictions.png")
    plt.close()

def forecast_prediction(variable, methodology, algorithm, feature_methodology, target_methodology, resample_name=""):
    start_time = time.time()
    features = methodology[[feature_methodology]].dropna()
    target = methodology[target_methodology]
    model = algorithm.fit(features, target)
    predictions = model.predict(features)
    mse = ((predictions - target) ** 2).mean()
    mape = mean_absolute_error(target, predictions) / target.abs().mean() * 100
    end_time = time.time() 
    print(f"{algorithm_name} - {methodology_name} - {resample_name} - {variable} MSE={str(mse)}, MAPE={str(mape)}%")
    print(f"Runtime:  {end_time-start_time}")
    plot_predicted_graph(target, variable, predictions, algorithm_name, methodology_name, resample_name)

def predict_methology(methodology, variable):
    features = methodology[[variable]]
    target = methodology[variable]
    model = algorithm.fit(features, target)
    predictions = model.predict(features)
    mse = ((predictions - target) ** 2).mean()
    mape = mean_absolute_error(target, predictions) / target.abs().mean() * 100
    return mse, mape, target, predictions

def historical_data_prediction(variable, methodology):
    start_time = time.time()
    mse, mape, target, predictions = predict_methology(methodology, variable)
    end_time = time.time() 
    print(f"{algorithm_name} - {methodology_name} (all data) - {variable}: MSE={str(mse)}, MAPE={str(mape)}%")
    print(f"Runtime:  {end_time-start_time}")
    plot_predicted_graph(target, variable, predictions, algorithm_name, methodology_name, resample_name="")

def predict_resample_methodology(resample_name, resample_methodology):
    if 'Temperature_Forecast' in resample_methodology.columns:
        start_time = time.time()
        features = resample_methodology[['Temperature_Forecast']].dropna()                    
        target = resample_methodology['Temperature'].dropna()
        model = algorithm.fit(features, target)
        predictions = model.predict(features)
        mse = ((predictions - target) ** 2).mean()
        mape = mean_absolute_error(target, predictions) / target.abs().mean() * 100
        end_time = time.time()
        print(f"{algorithm_name} - {methodology_name} {resample_name} - Temperature: MSE={str(mse)}, MAPE={str(mape)}%")
        print(f"Runtime:  {end_time-start_time}")
        plt.figure(figsize=(10, 5))
        plt.plot(target.index, target, label='Ground Truth')
        plt.plot(target.index, predictions, label='Predictions', linestyle='--')
        plt.title(f"Predicting temperature using {algorithm_name} with {methodology_name} and {resample_name}")
        plt.xlabel('Time')
        plt.ylabel('Temperature (°C)')
        plt.legend()
        plt.grid(True)
        #plt.show()
        plt.savefig(f"Temperature_{algorithm_name}_{methodology_name}_{resample_name}_forecast_predictions.png")
        plt.close()
    for variable in numeric_columns:
        start_time = time.time()
        features = resample_methodology[[variable]]
        target = resample_methodology[variable]
        target = target.dropna()
        features = features.dropna()
        model = algorithm.fit(features, target)
        predictions = model.predict(features)
        mse = ((predictions - target) ** 2).mean()
        mape = mean_absolute_error(target, predictions) / target.abs().mean() * 100
        end_time = time.time()
        print(f"{algorithm_name} - {methodology_name} ({resample_name}) - ({variable}): MSE={str(mse)}, MAPE={str(mape)}%")
        print(f"Runtime:  {end_time-start_time}")
        plt.figure(figsize=(10, 5))
        plt.plot(target.index, target, label='Ground Truth')
        plt.plot(target.index, predictions, label='Predictions', linestyle='--')
        plt.title(f"Predicting {variable} using {algorithm_name} with {methodology_name} and {resample_name}")
        plt.xlabel('Time')
        y_label = set_ylabel(variable)
        plt.ylabel(y_label)
        plt.legend()
        plt.grid(True)
        #plt.show()
        plt.savefig(f"{variable}_{algorithm_name}_{methodology_name}_{resample_name}_predictions.png")
        plt.close()

# Train models and make predictions
for algorithm_name, algorithm in algorithms.items():
    for methodology_name, methodology in methodologies.items():
        if isinstance(methodology, pd.DataFrame):
            
            if 'Temperature_Forecast' in methodology.columns:
                forecast_prediction("Temperature", methodology, algorithm, 'Temperature_Forecast', 'Temperature')
                
            # Training for other variables using their historical values
            for variable in numeric_columns:
                historical_data_prediction(variable, methodology)
        
        else:
            for resample_name, resample_methodology in methodology.items():
                
                predict_resample_methodology(resample_name, resample_methodology)

