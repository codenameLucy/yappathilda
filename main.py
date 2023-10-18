import asyncio
import json

from elevenlabs.elevenlabs_api import ElevenLabsAPI
from twitch.socket.twitch_socket import TwitchRewardSocket

with open("config/config.json") as config_file:
    config_contents = config_file.read()
json_config = json.loads(config_contents)


elevenlabs_api = ElevenLabsAPI(json_config=json_config)
twitch_socket = TwitchRewardSocket(json_config=json_config, elevenlabs_api=elevenlabs_api)


async def main():
    twitch_socket_task = asyncio.create_task(twitch_socket.listen())

    await asyncio.gather(twitch_socket_task)


if __name__ == "__main__":
    asyncio.run(main())
