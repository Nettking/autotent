# Digital Twin Project
## Overview
This repository contains the source code and related resources for the Digital Twin project, which simulates and predicts environmental conditions using IoT data, machine learning, and MQTT communications.

## Project Structure
The project is organized into three main directories:

### 1. Digital Twin
Contains the core functionality including models, monitoring scripts, and MQTT communication handlers. Key components:

Model: ThingML configurations and model simulations.
Monitor: Python scripts for forecasting and controlling environmental conditions.
MQTT: Scripts for handling MQTT communications including data publication and reception.

### 2. Machine Learning
Holds scripts and data related to machine learning models used for forecasting and image analysis. Components:

Forecast: Scripts for weather prediction and data analysis.
Image Analysis: Scripts for processing and analyzing images, including pixel counting and leaf detection.

### 3. ThingML-Gen
Contains Java-based tooling for generating code from ThingML models.

## Usage
### Running the Model
Navigate to the digital_twin/model directory:
java -jar model.jar

### Monitoring Scripts
For environmental monitoring, run:
python digital_twin/monitor/forecast.py

### MQTT Communication
Start the MQTT data receiver with:
python digital_twin/MQTT/communication/recieve_sensor_data.py

