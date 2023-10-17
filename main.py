import asyncio
import json

from elevenlabs.elevenlabs_api import ElevenLabsAPI
from elevenlabs.tts import play_audio
from twitch.socket.twitch_socket import TwitchRewardSocket

with open("config/config.json") as config_file:
    config_contents = config_file.read()
json_config = json.loads(config_contents)


elevenlabs_api = ElevenLabsAPI("b295d3a1d4b6ad97798ed8deda6a2fa1")
twitch_socket = TwitchRewardSocket(json_config=json_config, elevenlabs_api=elevenlabs_api)


async def main():
    twitch_socket_task = asyncio.create_task(twitch_socket.listen())

    await asyncio.gather(twitch_socket_task)


if __name__ == "__main__":
    asyncio.run(main())
