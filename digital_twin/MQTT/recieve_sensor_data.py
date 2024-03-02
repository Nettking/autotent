import csv
import json
from datetime import datetime, timezone
import paho.mqtt.client as mqtt

# MQTT broker details
mqtt_broker = "mqtt.eclipse.org"
mqtt_port = 1883
mqtt_topic = "sensor_data"

# CSV file to store received data
output_csv_file = "received_sensor_data.csv"

# Callback when a message is received from the MQTT broker
def on_message(client, userdata, msg):
    payload = msg.payload.decode("utf-8")
    sensor_data = json.loads(payload)

    # Convert Unix timestamp back to human-readable timestamp
    timestamp_str = datetime.fromtimestamp(sensor_data['Timestamp'], timezone.utc).strftime("%Y/%m/%d %H:%M:%S")
    sensor_data['Timestamp'] = timestamp_str

    # Append the received data to the CSV file
    with open(output_csv_file, 'a', newline='') as csvfile:
        fieldnames = ['Timestamp', 'Timezone', 'Temperature', 'Humidity', 'CO2', 'Noise', 'Pressure']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header if the file is empty
        if csvfile.tell() == 0:
            writer.writeheader()

        writer.writerow(sensor_data)
        print(f"Received and stored: {sensor_data}")

# Callback when connection is established
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(mqtt_topic)

# Main script
if __name__ == "__main__":
    # Create MQTT client instance
    client = mqtt.Client()

    # Set the callback functions
    client.on_connect = on_connect
    client.on_message = on_message

    # Connect to MQTT broker
    client.connect(mqtt_broker, mqtt_port, 60)

    # Loop to maintain the connection
    client.loop_forever()
