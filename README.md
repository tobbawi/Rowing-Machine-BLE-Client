# Virtufit Ultimate Pro 2i Rowing Machine Client + Strava Upload

This project is a client designed to connect to a Virtufit Ultimate Pro 2i rowing machine and upload rowing results to Strava. The client uses the latest Bluetooth FTMS (Fitness Machine Service) standards to ensure compatibility and accurate data transfer.

## Features

- Connects to Virtufit Ultimate Pro 2i rowing machine via Bluetooth
- Reads and processes rowing data
- Saves rowing data in TCX (Training Center XML) format
- Uploads TCX files to Strava
- Utilizes the latest Bluetooth FTMS standards

## Installation

To use this project, you need to have Python installed. You can install the required dependencies using pip:

```bash
pip install bleak
```

## Configuration

Before running the client, you need to configure two variables in the `const.py` file:

- `TARGET_DEVICE_NAME`: The name of your Virtufit Ultimate Pro 2i rowing machine
- `ROWING_TRAINER_CHARACTERISTIC_UUID`: The UUID of the characteristic used to receive rowing data

## Usage

1. Make sure your rowing machine is turned on and Bluetooth is activated
2. Run the script:

```bash
python main.py
```

3. The client will automatically connect to your rowing machine and start collecting data
4. After completing your rowing session, the script will save the data in a TCX file
5. If you have configured Strava integration, the script will automatically upload the session to your Strava account

## Strava Integration

To upload your rowing sessions to Strava, you first need to configure Strava API access:

1. Create a Strava API application at [https://www.strava.com/settings/api](https://www.strava.com/settings/api)
2. Note your Client ID and Client Secret
3. Add this information to the `config.py` file:

```python
STRAVA_CLIENT_ID = "your_client_id"
STRAVA_CLIENT_SECRET = "your_client_secret"
```

4. Run the authentication script to obtain an access token:

```bash
python strava_auth.py
```

5. Follow the instructions to authorize your Strava account

## Contributing

Contributions to this project are welcome! If you find a bug or want to propose a new feature, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Disclaimer

This project is not officially associated with or endorsed by Virtufit or Strava. Use it at your own risk.