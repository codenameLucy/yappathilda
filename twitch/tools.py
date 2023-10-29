import json
import logging
import webbrowser

import requests

logger = logging.getLogger(__name__)


def get_authentication_code(twitch_credentials: dict):
    parameters = (f"response_type=code&"
                  f"client_id={twitch_credentials['client_id']}&"
                  f"redirect_uri=http://localhost:7000&scope=channel:read:redemptions&"
                  f"state=c3ab8aa609ea11e793ae92361f002671")
    webbrowser.open(f'https://id.twitch.tv/oauth2/authorize?{parameters}')


def get_channel_id(twitch_credentials: dict) -> str:
    url = f"https://api.twitch.tv/helix/users?login={twitch_credentials['username']}"
    response = requests.get(url, headers={
        'Client-ID': twitch_credentials['client_id'],
        'Authorization': f"Bearer {twitch_credentials['auth_token']}"
    })
    data = response.json()

    if 'data' in data and data['data']:
        # Extract the channel ID
        return data['data'][0]['id']

    else:
        logger.critical(f"Username not found on twitch, please make sure you've given the correct name in the config")


def generate_twitch_token(twitch_credentials: dict) -> None:
    url = "https://id.twitch.tv/oauth2/token"

    data = {
        "client_id": twitch_credentials['client_id'],
        "client_secret": twitch_credentials['client_secret'],
        "code": twitch_credentials['code'],
        "grant_type": "authorization_code",
        "redirect_uri": "http://localhost:7000"
    }

    response = requests.post(url, data=data)

    with open("config/config.json", "r") as jsonFile:
        data = json.load(jsonFile)

    data["twitch_credentials"]['auth_token'] = response.json()['access_token']
    data["twitch_credentials"]["channel_id"] = get_channel_id(data["twitch_credentials"])

    with open("config/config.json", "w") as jsonFile:
        json.dump(data, jsonFile)
