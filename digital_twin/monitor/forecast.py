import numpy as np
from sklearn.linear_model import LinearRegression
import pandas as pd

# Sample data generation for demonstration
# In a real scenario, this data would come from actual sensors over time
np.random.seed(0)
hours = np.arange(0, 100)  # Last 100 hours
temperature = 20 + np.random.normal(0, 1, 100)  # Random temperature data
humidity = 50 + np.random.normal(0, 2, 100)  # Random humidity data
co2 = 400 + np.random.normal(0, 5, 100)  # Random CO2 data

# Optimal range for each parameter (this would be loaded from your CSV)
optimal_ranges = {
    'temperature': (18, 22),
    'humidity': (45, 55),
    'co2': (380, 420),
}

# Forecasting function
def forecast_next_day_values(X, y):
    model = LinearRegression()
    model.fit(X.reshape(-1, 1), y)
    # Predict the next 24 values (the next 24 hours)
    return model.predict(np.arange(101, 125).reshape(-1, 1))

# Forecast for each parameter
forecasted_temps = forecast_next_day_values(hours, temperature)
forecasted_humidity = forecast_next_day_values(hours, humidity)
forecasted_co2 = forecast_next_day_values(hours, co2)

# Check forecasted values against optimal ranges
def check_optimal_ranges(forecasted_values, parameter_name):
    min_val, max_val = optimal_ranges[parameter_name]
    for i, val in enumerate(forecasted_values, start=1):
        if val < min_val or val > max_val:
            print(f"Warning: Forecasted {parameter_name} at hour {i} is outside the optimal range ({min_val}, {max_val}). Value: {val:.2f}")

check_optimal_ranges(forecasted_temps, 'temperature')
check_optimal_ranges(forecasted_humidity, 'humidity')
check_optimal_ranges(forecasted_co2, 'co2')
