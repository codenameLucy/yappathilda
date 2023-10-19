import asyncio
import json
import logging

from elevenlabs.elevenlabs_api import ElevenLabsAPI
from tools.initial_setup_checkers import check_config_available, check_obs_setup, check_twitch_websocket_connection, \
    check_elevenlabs_voice_setup
from twitch.socket.twitch_socket import TwitchRewardSocket

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main(json_config: dict):
    elevenlabs_api = ElevenLabsAPI(elevenlabs_credentials=json_config['elevenlabs_credentials'])
    twitch_socket = TwitchRewardSocket(json_config=json_config, elevenlabs_api=elevenlabs_api)

    twitch_socket_task = asyncio.create_task(twitch_socket.listen())

    await asyncio.gather(twitch_socket_task)


if __name__ == "__main__":
    initial_setup = False

    logger.info("Commencing initial check")

    while not initial_setup:
        cnfg = check_config_available(file_path="config/config.json")

        # once we know config is available, read out
        if cnfg:
            with open("config/config.json") as config_file:
                config_contents = config_file.read()
            json_config = json.loads(config_contents)

            obs = check_obs_setup(obs_credentials=json_config['obs_credentials'])
            ttv = check_twitch_websocket_connection(twitch_credentials=json_config['twitch_credentials'])
            x_ii = check_elevenlabs_voice_setup(elevenlabs_credentials=json_config['elevenlabs_credentials'])

            # go to main program once ensured everything is in place
            if obs and ttv and x_ii:
                initial_setup = True
            else:
                input("press enter to retry setup")

    try:
        asyncio.run(main(json_config=json_config))
    except Exception as e:
        logger.critical(f"[Oopsie Woopsie :3] an ewwow has occuwed: {e}")
        input("press enter to close")
