import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np

# Load room data
room_data = pd.read_csv("room_data.csv", delimiter=";")
room_data["Timestamp"] = pd.to_datetime(room_data["Timestamp"])  # Adjust the column name if necessary
room_data.set_index("Timestamp", inplace=True)

# Assume 'Temperature' is a numeric column
room_data = room_data[['Temperature']]

def generate_features_and_labels(data, feature_points, forecast_horizon):
    X, y = [], []
    for i in range(feature_points, len(data) - forecast_horizon):
        X.append(data['Temperature'].iloc[i-feature_points:i].values)
        y.append(data['Temperature'].iloc[i + forecast_horizon])
    return X, y

# Generate features and labels for 6 data points and a forecast 6 hours ahead
X, y = generate_features_and_labels(room_data, 6, 12)
# Convert lists to arrays for model training

X = np.array(X)
y = np.array(y)

# Train the Linear Regression model
model = LinearRegression()
model.fit(X, y)
# Predict using the same data (for illustration, typically you'd use unseen test data)
predictions = model.predict(X)

from sklearn.metrics import mean_squared_error, mean_absolute_error

mse = mean_squared_error(y, predictions)
mape = mean_absolute_error(y, predictions) / np.mean(np.abs(y)) * 100

print(f"MSE: {mse}, MAPE: {mape}%")

# Plotting
plt.figure(figsize=(15, 7))
plt.plot(y, label='Actual Temperature', color='blue')
plt.plot(predictions, label='Predicted Temperature', color='red', linestyle='--')
plt.title('Temperature Forecast vs Actual')
plt.xlabel('Time (in hours)')
plt.ylabel('Temperature (°C)')
plt.legend()
plt.show()

