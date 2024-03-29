import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# Load dataset
data = pd.read_csv("temp.csv")

# Convert timestamp to numerical representation (Unix timestamp)
data['Timestamp'] = pd.to_datetime(data['Timestamp'], unit='s').astype('int64')

# Split dataset into features (X) and target variable (y)
X = data[['Timestamp']]  # Using only 'Timestamp' as predictor variable
y = data['Temperature']

# Split dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the SVR model
model = SVR(kernel='rbf')  # Radial Basis Function (RBF) kernel is commonly used for SVR
model.fit(X_train, y_train)

# Make predictions on the testing set
y_pred = model.predict(X_test)

# Calculate Mean Squared Error
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)

# Plot actual vs predicted temperature
plt.figure(figsize=(10, 6))
plt.scatter(X_test, y_test, color='blue', label='Actual Temperature')
plt.plot(X_test, y_pred, color='red', label='Predicted Temperature')
plt.title('SVR: Actual vs Predicted Temperature')
plt.xlabel('Timestamp')
plt.ylabel('Temperature')
plt.legend()
plt.show()
