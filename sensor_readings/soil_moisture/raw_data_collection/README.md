# Arduino Sensor Experiment

This part of the repository contains the code and details of an experiment aimed at studying the deterioration of sensors over a span of 5 weeks. Over the course of this period, two new sensors are introduced each week, making a total of 10 sensors by the end. The experiment studies how the error rates change over time and if taking more frequent readings leads to faster deterioration. To compare the error rates Fruugo Pms710 was used to compare. 

## Fruugo Pms710
Humidity:5%-90%RH
Resolusion:0.1
Accuracy: 2%n(Non-saturation condition)

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features
- Ability to read data from up to 10 sensors.
- Takes two sets of readings daily: one with 3 readings and another with 10 readings, to compare the impact of reading frequency.
- Humidity is determined using a linear interpolation, where a sensorValue of 0 corresponds to 0% humidity (completely dry) and a sensorValue of 1024 corresponds to 100% humidity (completely wet).
- Timestamps are stored in UNIX format for ease of analysis.

## Requirements
- Arduino Mega 2560
- Sensors:
  - 10 x TZT HL-69 Humidity Probe Sensor
  - An accurate sensor to compare humidity 

## Installation
1. Clone this repository:
git clone [your-repository-link]

2. Install the required Arduino libraries. You can do this via the Arduino IDE Library Manager or by downloading the ZIP files and adding them manually.

3. Load the Arduino sketch onto your board using the Arduino IDE.

## Usage
1. Connect the sensors to your Arduino board. The connections are detailed in [a link to a schematic or a section detailing the connections].
2. Power on the Arduino.
3. Open the Serial Monitor to view the sensor readings and to confirm successful data recording to the SD card.
4. To analyze the recorded data, use the accompanying Python script. This script will process the readings and calculate errors based on user-input reference readings. The resulting data will provide insights into the deterioration trend of the sensors over the 5-week period. The user must input the sensor readings from the soil moisture sensor.


