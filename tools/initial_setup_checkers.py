import json
import os
import logging
from json import JSONDecodeError

from websockets.sync.client import connect

from elevenlabs.elevenlabs_api import ElevenLabsAPI, VoiceNotFoundException
from obs.obs_websocket import OBSWebsocket, OBSConnectionFailedException, OBSSceneMissingException
from tools.twitch_auth_generator import initialize_flask_twitch_authentication
from twitch.tools import generate_twitch_token, TwitchUserNotFoundException

logger = logging.getLogger(__name__)


def validate_setup():
    cnfg = check_config_available(file_path="config/config.json")

    # once we know config is available, read out
    if cnfg:
        try:
            with open("config/config.json") as config_file:
                json_config = json.loads(config_file.read())
        except JSONDecodeError as e:
            logger.critical(f" [ERROR] An exception happened during validation of the config, nerd code: {e}")
            return False

        if not json_config['twitch_credentials'].get("channel_id"):
            logger.warning(" [OK] Twitch credentials missing, starting authentication process...")
            initialize_flask_twitch_authentication(twitch_credentials=json_config['twitch_credentials'])
            with open("config/config.json") as config_file:
                json_config = json.loads(config_file.read())
            try:
                generate_twitch_token(json_config=json_config)
            except TwitchUserNotFoundException:
                logger.critical(
                    " [ERROR] Username not found on twitch, "
                    "please make sure you've given the correct name in the config"
                )
                return False

        obs = check_obs_setup(obs_credentials=json_config['obs_credentials'])
        ttv = check_twitch_websocket_connection(twitch_credentials=json_config['twitch_credentials'])
        x_ii = check_elevenlabs_voice_setup(elevenlabs_credentials=json_config['elevenlabs_credentials'])

        # go to main program once ensured everything is in place
        if obs and ttv and x_ii:
            return True
        return False


def check_config_available(file_path: str) -> bool:
    if os.path.exists(file_path):
        logger.info(" [OK] Config found")
        return True
    logger.critical(
        " [ERROR] Config file can not be found, "
        "check your config folder and make sure you renamed config.json.example to config.json"
    )
    return False


def check_obs_setup(obs_credentials: dict) -> bool:
    try:
        obs_web_socket = OBSWebsocket(obs_credentials=obs_credentials)
    except OBSConnectionFailedException as e:
        logger.critical(f" [ERROR] {e}")
        return False
    logger.info(" [OK] OBS running and connection to websocket established")
    try:
        obs_web_socket.get_scene_item_id()
    except OBSSceneMissingException as e:
        logger.critical(f" [OK] Scenes not found, creating...")
        obs_web_socket.create_tts_sources()
    logger.info(" [OK] OBS scenes and sources set up correctly")
    return True


def check_twitch_websocket_connection(twitch_credentials: dict) -> bool:
    with connect(twitch_credentials['server']) as websocket:
        # Send a message to the server to listen to a specific topic
        websocket.send(json.dumps({
            "type": "LISTEN",
            "data": {
                "topics": [f"channel-points-channel-v1.{twitch_credentials['channel_id']}"],
                "auth_token": twitch_credentials['auth_token']
            }
        }))
        if json.loads(websocket.recv()).get("error") == "ERR_BADAUTH":
            logger.critical(
                " [ERROR] Connection with twitch failed, "
                "make sure your channel_id and auth_token are correct in config"
            )
            return False
        logger.info(" [OK] Twitch websocket properly configured")
        return True


def check_elevenlabs_voice_setup(elevenlabs_credentials: dict) -> bool:
    xi_api = ElevenLabsAPI(elevenlabs_credentials=elevenlabs_credentials)
    try:
        xi_api.get_voice_id(elevenlabs_credentials['voice_name'])
    except VoiceNotFoundException as e:
        logger.critical(f" [ERROR] {e}")
        return False
    return True
