import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('temp.csv')

# Convert the timestamp to a datetime format and create a numerical feature for the model
df['Datetime'] = pd.to_datetime(df['Timestamp'], unit='s')
df['Time_in_minutes'] = (df['Datetime'] - df['Datetime'].min()).dt.total_seconds() / 60

# Split the data - this logic assumes you have continuous data and will need adjustment for your specific case
last_7_days_mask = df['Datetime'] > (df['Datetime'].max() - pd.Timedelta(days=7))
train_data = df[~last_7_days_mask]
test_data = df[last_7_days_mask]

# Train the linear regression model
model = LinearRegression()
model.fit(train_data[['Time_in_minutes']], train_data['Temperature'])

# Predict temperatures for the test set
predictions = model.predict(test_data[['Time_in_minutes']])
test_data['Predicted_Temperature'] = predictions

# Evaluate the model
mse = mean_squared_error(test_data['Temperature'], predictions)
mae = mean_absolute_error(test_data['Temperature'], predictions)
print(f'Mean Squared Error: {mse}')
print(f'Mean Absolute Error: {mae}')

# Plotting only the test data and predictions
plt.figure(figsize=(10, 6))
plt.plot(test_data['Datetime'], test_data['Temperature'], label='Actual Temperature')
plt.plot(test_data['Datetime'], test_data['Predicted_Temperature'], label='Predicted Temperature', linestyle='--')
plt.xlabel('Date')
plt.ylabel('Temperature')
plt.title('Temperature Prediction for the Last 7 Days')
plt.legend()
plt.show()
