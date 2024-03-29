import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv('temp2.csv')
df['Timezone : Europe/Oslo'] = pd.to_datetime(df['Timezone : Europe/Oslo'])

# Convert timestamp to a numerical feature (minutes since start)
df['Minutes'] = (df['Timezone : Europe/Oslo'] - df['Timezone : Europe/Oslo'].min()).dt.total_seconds() / 60

# Split the data into training and testing sets (last 7 days for testing)
# Note: Adjust the 7-day split based on the actual frequency of your data
train_df = df[df['Timezone : Europe/Oslo'] < df['Timezone : Europe/Oslo'].max() - pd.Timedelta(days=7)]
test_df = df[df['Timezone : Europe/Oslo'] >= df['Timezone : Europe/Oslo'].max() - pd.Timedelta(days=7)]

# Train the model
model = LinearRegression()
model.fit(train_df[['Minutes']], train_df['Temperature'])

# Predict the temperature
test_df['Predicted'] = model.predict(test_df[['Minutes']])

# Calculate the percentage error
test_df['Error%'] = 100 * abs(test_df['Temperature'] - test_df['Predicted']) / test_df['Temperature']

# Output the mean percentage error
mean_percentage_error = test_df['Error%'].mean()
print(f"Mean Percentage Error: {mean_percentage_error}%")

# Plotting the results
plt.figure(figsize=(10, 6))
plt.plot(df['Timezone : Europe/Oslo'], df['Temperature'], label='Actual Temperature')
plt.plot(test_df['Timezone : Europe/Oslo'], test_df['Predicted'], label='Predicted Temperature')
plt.xlabel('Time')
plt.ylabel('Temperature')
plt.title('Temperature Prediction')
plt.legend()
plt.show()
