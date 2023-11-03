import numpy as np
import matplotlib.pyplot as plt

# Define the base optimal conditions for strawberry growth
optimal_conditions = {
    'temperature': 20,  # Optimal temperature in degrees Celsius
    'sunlight': 8,      # Optimal sunlight in hours
    'soil_moisture': 25 # Optimal soil moisture in percentage
}

# Function to calculate growth rate modifier based on deviation from optimal conditions
def growth_rate_modifier(value, optimal, range_tolerance):
    """Calculate a modifier for growth rate based on the deviation from optimal conditions."""
    # Assume that the growth rate decreases linearly outside the optimal range by 10% per unit
    return 1 - 0.1 * abs(value - optimal) / range_tolerance

# Function to simulate daily growth rate
def simulate_daily_growth(temperature, sunlight, soil_moisture):
    """
    Simulate the daily growth rate of strawberry plants based on temperature, sunlight, and soil moisture.
    The growth rate is a percentage, with 1.0 representing 100%.
    """
    # Define the range tolerance for each condition
    temperature_tolerance = 10  # degrees Celsius
    sunlight_tolerance = 4      # hours
    soil_moisture_tolerance = 10 # percentage points
    
    # Calculate growth rate modifiers for each condition
    temp_modifier = growth_rate_modifier(temperature, optimal_conditions['temperature'], temperature_tolerance)
    sunlight_modifier = growth_rate_modifier(sunlight, optimal_conditions['sunlight'], sunlight_tolerance)
    soil_moisture_modifier = growth_rate_modifier(soil_moisture, optimal_conditions['soil_moisture'], soil_moisture_tolerance)
    
    # Assume the base growth rate is 5% under optimal conditions
    base_growth_rate = 0.05
    
    # Calculate the combined growth rate
    combined_growth_rate = base_growth_rate * temp_modifier * sunlight_modifier * soil_moisture_modifier
    
    return combined_growth_rate

# Example of data for a month (30 days), using random values around optimal conditions
np.random.seed(0)  # For reproducibility
example_temperatures = np.random.normal(loc=optimal_conditions['temperature'], scale=5, size=30)
example_sunlight = np.random.normal(loc=optimal_conditions['sunlight'], scale=2, size=30)
example_soil_moisture = np.random.normal(loc=optimal_conditions['soil_moisture'], scale=5, size=30)

# Simulate the growth rate for each day
daily_growth_rates = [simulate_daily_growth(temp, sun, moisture) for temp, sun, moisture in 
                      zip(example_temperatures, example_sunlight, example_soil_moisture)]

# Plot the simulated daily growth rates
plt.figure(figsize=(14, 7))
plt.plot(daily_growth_rates, marker='o')
plt.title('Simulated Daily Growth Rates of Strawberry Plants Over a Month')
plt.xlabel('Day')
plt.ylabel('Growth Rate (%)')
plt.grid(True)
plt.show()
