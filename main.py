import asyncio
import json
import logging

from elevenlabs.elevenlabs_api import ElevenLabsAPI
from tools.initial_setup_checkers import check_config_available, check_obs_setup, check_twitch_websocket_connection, \
    check_elevenlabs_voice_setup, validate_setup
from tools.twitch_auth_generator import initialize_flask_twitch_authentication
from twitch.socket.twitch_socket import TwitchRewardSocket
from twitch.tools import generate_twitch_token

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():

    with open("config/config.json") as config_file:
        json_config = json.loads(config_file.read())

    elevenlabs_api = ElevenLabsAPI(elevenlabs_credentials=json_config['elevenlabs_credentials'])
    twitch_socket = TwitchRewardSocket(json_config=json_config, elevenlabs_api=elevenlabs_api)

    twitch_socket_task = asyncio.create_task(twitch_socket.listen())

    await asyncio.gather(twitch_socket_task)


if __name__ == "__main__":
    initial_setup = False
    logger.info("Commencing initial check")

    while not initial_setup:
       initial_setup = validate_setup()
       if not initial_setup:
           input("Something went wrong during inital setup, please check the error and try again by pressing enter...")

    try:
        asyncio.run(main())
    except Exception as e:
        logger.critical(f"[Oopsie Woopsie :3] an ewwow has occuwed: {e}")
        input("press enter to close")
