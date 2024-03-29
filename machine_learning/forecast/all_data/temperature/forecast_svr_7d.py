import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# Load room data
room_data = pd.read_csv("room_data.csv", delimiter=";")
room_data["Timestamp"] = pd.to_datetime(room_data["Timezone : Europe/Oslo"])

# Extract temperature data
room_data_hourly = room_data[["Timestamp", "Temperature"]]
room_data_hourly.set_index("Timestamp", inplace=True)

# Splitting data into training and testing sets
training_data = room_data_hourly.iloc[:-24*7]  # All but the last 7 days
testing_data = room_data_hourly.iloc[-24*7:]

# Preparing data for modeling
X_train = training_data.index.values.reshape(-1, 1)
y_train = training_data["Temperature"]
X_test = testing_data.index.values.reshape(-1, 1)
y_test = testing_data["Temperature"]

# Train the linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions
predictions = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, predictions)
print(f"Mean Squared Error: {mse}")

# Plotting predicted values vs real values
plt.figure(figsize=(10, 6))
plt.plot(testing_data.index, y_test, label="Real Values", color='blue')
plt.plot(testing_data.index, predictions, label="Predicted Values", color='red')
plt.xlabel("Timestamp")
plt.ylabel("Temperature")
plt.title("Temperature - Real vs Predicted Values (Last 7 Days)")
plt.legend()
plt.show()
