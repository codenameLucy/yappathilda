import asyncio
import json

from elevenlabs.elevenlabs_api import ElevenLabsAPI
from twitch.socket.twitch_socket import TwitchRewardSocket


async def main():
    try:
        with open("config/config.json") as config_file:
            config_contents = config_file.read()
    except FileNotFoundError as e:
        raise FileNotFoundError(e) from e
    json_config = json.loads(config_contents)

    elevenlabs_api = ElevenLabsAPI(json_config=json_config)
    twitch_socket = TwitchRewardSocket(json_config=json_config, elevenlabs_api=elevenlabs_api)

    twitch_socket_task = asyncio.create_task(twitch_socket.listen())

    await asyncio.gather(twitch_socket_task)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"[Oopsie Woopsie :3] an ewwow has occuwed: {e}")
        input("press enter to close")
