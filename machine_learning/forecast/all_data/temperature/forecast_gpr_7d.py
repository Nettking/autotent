import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.random_projection import GaussianRandomProjection
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error

# Load room data
room_data = pd.read_csv("room_data.csv", delimiter=";")
room_data["Timestamp"] = pd.to_datetime(room_data["Timezone : Europe/Oslo"])

# Exclude non-numeric columns from aggregation
numeric_columns = ["Temperature", "Humidity", "CO2", "Noise", "Pressure"]
room_data_numeric = room_data[["Timestamp"] + numeric_columns]

# Aggregate room data to hourly averages and convert to appropriate data type
room_data_hourly = room_data_numeric.resample('H', on='Timestamp').mean().astype(float)

# Reset index to make 'Timestamp' a regular column again
room_data_hourly.reset_index(inplace=True)

training_data = room_data_hourly.iloc[:-24*7]  # All but the last 7 days
testing_data = room_data_hourly.iloc[-24*7:]

# Feature selection
X_train = training_data.drop(columns=["Timestamp"] + numeric_columns)
X_test = testing_data.drop(columns=["Timestamp"] + numeric_columns)

# Target variables
y_train = training_data[numeric_columns]
y_test = testing_data[numeric_columns]

# Feature selection
X_train = training_data.drop(columns=["Timestamp"] + numeric_columns)
X_test = testing_data.drop(columns=["Timestamp"] + numeric_columns)

# Ensure X_train is not empty and contains only numeric data
if X_train.empty:
    raise ValueError("X_train is empty. Check your feature selection process.")
if not all(isinstance(dtype, np.number) for dtype in X_train.dtypes):
    raise TypeError("X_train contains non-numeric data types.")

# Applying Gaussian Random Projection
grp = GaussianRandomProjection()
X_train_reduced = grp.fit_transform(X_train)
X_test_reduced = grp.transform(X_test)

# Applying Gaussian Random Projection
grp = GaussianRandomProjection()
X_train_reduced = grp.fit_transform(X_train)
X_test_reduced = grp.transform(X_test)

# Train the linear regression model for each variable
models = {}
for variable in numeric_columns:
    model = LinearRegression()
    model.fit(X_train_reduced, y_train[variable])
    models[variable] = model

# Make predictions for the testing data
predictions = pd.DataFrame({variable: models[variable].predict(X_test_reduced) for variable in numeric_columns})

# Evaluate the model using Mean Squared Error (MSE)
mse_scores = {variable: mean_squared_error(y_test[variable], predictions[variable]) for variable in numeric_columns}
print("Mean Squared Error for each variable:")
for variable, mse in mse_scores.items():
    print(f"{variable}: {mse}")

average_mse = np.mean(list(mse_scores.values()))
print(f"Average Mean Squared Error: {average_mse}")

# Plotting predicted values vs real values for each variable
for variable in numeric_columns:
    plt.figure(figsize=(10, 6))
    plt.plot(testing_data["Timestamp"], y_test[variable], label="Real Values", color='blue')
    plt.plot(testing_data["Timestamp"], predictions[variable], label="Predicted Values", color='red')
    plt.xlabel("Timestamp")
    plt.ylabel(variable)
    plt.title(f"{variable} - Real vs Predicted Values (Last 7 Days)")
    plt.legend()
    plt.show()
