import json
import os
import logging

from websockets.sync.client import connect

from elevenlabs.elevenlabs_api import ElevenLabsAPI, VoiceNotFoundException
from obs.obs_websocket import OBSWebsocket, OBSConnectionFailedException, OBSSceneMissingException

logger = logging.getLogger(__name__)


def check_config_available(file_path: str) -> bool:
    if os.path.exists(file_path):
        logger.info(" [OK] Config found")
        return True
    logger.critical(
        " [ERROR] Config file can not be found, "
        "check your config folder and make sure you renamed config.json.exampl~e to config.json"
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
        obs_web_socket.get_scene_item_id(scene_name=obs_credentials['scene_name'],
                                         source_name=obs_credentials['source_name'])
    except OBSSceneMissingException as e:
        logger.critical(f" [ERROR] {e}")
        return False
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
