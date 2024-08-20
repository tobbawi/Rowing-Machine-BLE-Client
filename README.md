# Virtufit Ultimate Pro 2i Rowing Client + Upload to Strava

This project is a simple client designed to connect to a Virtufit Ultimate Pro 2i rowing machine and upload rowing results to Strava. The client uses the latest Bluetooth FTMS (Fitness Machine Service) standards to ensure compatibility and accurate data transfer.

## Features

- Connects to Virtufit Ultimate Pro 2i rowing machine via Bluetooth.
- Reads and processes rowing data.
- Saves rowing data in TCX (Training Center XML) format.
- Uploads TCX files to Strava.
- Utilizes the latest Bluetooth FTMS standards.

## Installation

To use this project, you need to have Python installed. You can install the required dependencies using pip:

```bash
pip install bleak
```

## Setup

Before running the client, you need to configure two variables in the const.py file:

TARGET_DEVICE_NAME: The name of your Virtufit Ultimate Pro 2i rowing machine.
ROWING_TRAINER_CHARACTERISTIC_UUID: The UUID of the characteristic used to receive rowing data.
