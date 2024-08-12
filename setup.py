import argparse
from flask import Flask, request, redirect
from stravalib.client import Client
import threading
import webbrowser
import pickle
import const

# Initialize Flask app
app = Flask(__name__)

# Define a global variable to store the client
client = Client()

# Function to handle the OAuth flow
@app.route('/authorized')
def authorized():
    code = request.args.get('code')
    if not code:
        return "Authorization failed. No code provided."

    print(f"Exchange code for token {code}")
    # Exchange the code for an access token
    token_response = client.exchange_code_for_token(
        client_id=client_id,
        client_secret=client_secret,
        code=code
    )

    # Access token details
    access_token = token_response['access_token']
    refresh_token = token_response['refresh_token']
    expires_at = token_response['expires_at']

    # Print the tokens for verification
    print("Access Token:", access_token)
    print("Refresh Token:", refresh_token)
    print("Expires At:", expires_at)

    with open(const.MY_STRAVA_ACCESS_TOKEN_FILE, 'wb') as f:
        pickle.dump(token_response, f)
        print("Access token saved!")
    
    return "Authorization successful! You can close this window."

def save_client_info(client_id, client_secret):
    client_info = {}
    client_info['client_id'] = client_id
    client_info['client_secret'] = client_secret
    with open(const.MY_STRAVA_CLIENT_INFO, 'wb') as f:
        pickle.dump(client_info, f)
        print(f'Client info saved: client_id {client_id} and client_secret {client_secret}')

def run_flask_app():
    app.run(port=8082)

def main():
    parser = argparse.ArgumentParser(description='Strava OAuth CLI Tool')
    parser.add_argument('--client-id', required=True, help='Strava Client ID')
    parser.add_argument('--client-secret', required=True, help='Strava Client Secret')
    args = parser.parse_args()

    global client_id, client_secret
    client_id = args.client_id
    client_secret = args.client_secret
    save_client_info(client_id, client_secret)

    # Configure the client
    global client
    client = Client()
    auth_url = client.authorization_url(
        client_id=client_id,
        redirect_uri='http://localhost:8082/authorized',
        scope=['read', 'activity:read', 'activity:write']
    )

    # Open the authorization URL in the default web browser
    webbrowser.open(auth_url)

    # Run the Flask app in a separate thread
    server_thread = threading.Thread(target=run_flask_app)
    server_thread.start()

if __name__ == '__main__':
    main()