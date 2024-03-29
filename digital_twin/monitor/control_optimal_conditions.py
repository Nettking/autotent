import paho.mqtt.client as mqtt
import pandas as pd

# Define the MQTT topic and the CSV file path
MQTT_TOPIC = "your/mqtt/topic"
CSV_FILE_PATH = "optimal_values.csv"

# Load the CSV file containing the optimal values
optimal_values_df = pd.read_csv(CSV_FILE_PATH)

# This function simulates processing the incoming MQTT message and updating the plant state
def process_message(message):
    # Simulate processing the MQTT message to extract plant state information
    # For demonstration, we'll assume message.payload is a dictionary containing the necessary information
    plant_state_info = eval(message.payload)  # This is for demonstration; in practice, use a secure method to parse the payload

    # Update the plant state based on the message
    current_plant_state = plant_state_info['current_plant_state']
    
    # Retrieve the optimal values for the current plant state from the CSV
    optimal_values = optimal_values_df[optimal_values_df['state'] == current_plant_state].iloc[0]

    # Check if any of the values are outside the optimal range and warn the user
    if not (optimal_values['optimal_temperature']['min'] <= plant_state_info['temperature'] <= optimal_values['optimal_temperature']['max']):
        print(f"Warning: Temperature is outside the optimal range for {current_plant_state} state.")
    
    # Repeat the above check for humidity and CO2

# The callback for when the client receives a CONNACK response from the server
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(MQTT_TOPIC)

# The callback for when a PUBLISH message is received from the server
def on_message(client, userdata, msg):
    print(f"Message received on topic {msg.topic}")
    process_message(msg)

# Set up the MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker (replace with your broker's IP/hostname and port)
client.connect("mqtt_broker_ip", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks, and handles reconnecting
client.loop_forever()
