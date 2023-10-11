# Image Collection from Raspberry Pi Cameras

This directory contains the `pictures.py` script, designed to automatically collect images from two Raspberry Pi devices, identified as the top camera and side camera. Each image is captured, transferred, renamed with the current date, and then stored, while the original image on the Raspberry Pi is deleted.

## Script Overview

### 1. pictures.py

#### Description:
The `pictures.py` script functions as follows:

- **Initialization**: On startup, the script logs the current date and time, indicating the monitoring commencement.

- **Image Collection**: The script fetches images from two distinct Raspberry Pi cameras (Top and Side). Each image is:
  1. Captured using `raspistill`.
  2. Copied over SSH using `scp` to the current system.
  3. Renamed with a date prefix and the camera's identifier.
  4. The original image on the Raspberry Pi is deleted.

- **Periodic Collection**: The script continuously checks the system time. Every day at 05:59, images are captured from both cameras and processed as described above.

#### Dependencies:
- The script assumes the Raspberry Pi devices are set up for passwordless SSH connections.
- Ensure the `subprocess` module is available in your Python environment.
  
#### Usage:
To run the script, navigate to its directory and use the following command:
python pictures.py

The script will then operate indefinitely, automatically capturing images each day at the specified time. Make sure the Raspberry Pi devices are accessible over the network during this period.

## Log Details:
Any significant event or error during the script's execution gets logged into a `log` file within the directory `/mnt/c/wsl/pictures/`. This includes successful image collections, connection failures, and image deletion errors.

## Important Notes:

1. **SSH Configuration**: Ensure the Raspberry Pi devices have SSH enabled and are set up for passwordless connections. This allows the script to seamlessly capture and transfer images without manual intervention.

2. **Storage Path**: The images and log file are stored at `/mnt/c/wsl/pictures/`. If you wish to change this location, modify the `run_directory` variable within the script.

3. **Error Handling**: While the script contains basic error handling, always monitor the `log` file to ensure smooth operations and troubleshoot any issues.