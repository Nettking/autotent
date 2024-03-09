import os
import pandas as pd
import matplotlib.pyplot as plt

# Read data from the CSV file
data_path = os.path.join('strawberries', "data.csv")
df = pd.read_csv(data_path)

def calculate_average_sizes_and_weights(dataframe):
    # Calculate average sizes
    average_height = dataframe["Height (cm)"].mean()
    average_width = dataframe["Width (cm)"].mean()
    average_diameter = dataframe["Diameter (cm)"].mean()

    # Calculate average weight
    average_weight = dataframe["Weight (g)"].mean()

    # Print the results
    print(f"Average Height: {average_height:.2f} cm")
    print(f"Average Width: {average_width:.2f} cm")
    print(f"Average Diameter: {average_diameter:.2f} cm")
    print(f"Average Weight: {average_weight:.2f} g")



# Convert the "Date" column to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Create subplots for size and weight
fig, axes = plt.subplots(2, 1, figsize=(12, 6))

# Plot size (height, width, diameter) against dates
df.plot(x="Date", y=["Height (cm)", "Width (cm)", "Diameter (cm)"], ax=axes[0])
axes[0].set_title("Strawberry Size Over Time")
axes[0].set_ylabel("Size (cm)")

# Plot weight against dates
df.plot(x="Date", y="Weight (g)", ax=axes[1], color="green")
axes[1].set_title("Strawberry Weight Over Time")
axes[1].set_ylabel("Weight (g)")

# Adjust plot layout
plt.tight_layout()

# Call the function to calculate and print the averages
calculate_average_sizes_and_weights(df)

# Show the plots
plt.show()
