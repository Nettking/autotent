import time
import random
import json
import paho.mqtt.client as mqtt

# MQTT broker details
mqtt_broker = "mqtt.eclipse.org"
mqtt_port = 1883
mqtt_topic = "sensor_data"

# Function to simulate sensor reading
def get_sensor_reading():
    # Replace this with your actual sensor reading logic
    return random.uniform(20.0, 30.0)

# Function to publish sensor reading on MQTT
def publish_sensor_reading(client, topic, reading):
    payload = json.dumps({"sensor_reading": reading})
    client.publish(topic, payload, qos=2)
    print(f"Published: {payload}")

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

    # Connect to MQTT broker
    client.connect(mqtt_broker, mqtt_port, 60)

    # Loop to maintain the connection
    client.loop_start()

    try:
        while True:
            # Get sensor reading
            sensor_reading = get_sensor_reading()

            # Publish sensor reading on MQTT
            publish_sensor_reading(client, mqtt_topic, sensor_reading)

            # Wait for some time before the next reading
            time.sleep(5)

    except KeyboardInterrupt:
        print("Script terminated by user.")
        client.disconnect()
        client.loop_stop()
