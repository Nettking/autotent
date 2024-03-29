import pandas as pd
from sklearn.linear_model import LinearRegression
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
X_train = training_data.drop(columns=["Timestamp"])
X_test = testing_data.drop(columns=["Timestamp"])

# Target variables
y_train = training_data[numeric_columns]
y_test = testing_data[numeric_columns]
# Drop rows with missing values
X_train.dropna(inplace=True)
y_train.dropna(inplace=True)

# Train the linear regression model for each variable, excluding the target variable from the features
models = {}
for variable in numeric_columns:
    # Exclude the current variable from the features for this iteration
    X_train_temp = X_train.drop(columns=[variable])
    X_test_temp = X_test.drop(columns=[variable])

    # Train model
    model = LinearRegression()
    model.fit(X_train_temp, y_train[variable])
    models[variable] = model

# Make predictions for the testing data
predictions = pd.DataFrame({variable: models[variable].predict(X_test.drop(columns=[variable])) for variable in numeric_columns})

# Evaluate the model (you might want to use a different evaluation metric for multi-variable predictions)
mse = ((predictions - y_test) ** 2).mean()
print(f"Mean Squared Error: {mse}")
print("Predictions:")
print(predictions.head())
print("\nActual Values:")
print(y_test.head())
print(mse)

mse_scores = {}
for variable in numeric_columns:
    y_true = y_test[variable]
    y_pred = predictions[variable]
    mse = mean_squared_error(y_true, y_pred)
    mse_scores[variable] = mse

print("Mean Squared Error for each variable:")
for variable, mse in mse_scores.items():
    print(f"{variable}: {mse}")
    


average_mse = sum(mse_scores.values()) / len(mse_scores)
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
