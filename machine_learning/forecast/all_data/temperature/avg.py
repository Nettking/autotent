import pandas as pd

# Load the data from 'room_data.csv'
df = pd.read_csv('room_data.csv', delimiter=';')

# Calculate and print the average of each numeric column
for column in ['Temperature', 'Humidity', 'CO2', 'Noise', 'Pressure']:
    average = df[column].mean()
    print(f"Average {column}: {average}")
