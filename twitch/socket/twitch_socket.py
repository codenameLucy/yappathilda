import json

import websockets

from elevenlabs.elevenlabs_api import ElevenLabsAPI
from elevenlabs.tts import play_audio


# TODO: Find a way for our programm to generate the channel token with the correct helix scope, currently used https://twitchtokengenerator.com/


# TODO: Find a way to automatically determine channel id of user


class TwitchRewardSocket:
    def __init__(self, json_config: dict, elevenlabs_api: ElevenLabsAPI):
        self.json_config = json_config
        # Set Twitch credentials
        credentials = self.json_config['twitch_credentials']
        channel_id = credentials['channel_id']
        self.topics = [f"channel-points-channel-v1.{channel_id}"]
        self.auth_token = credentials['auth_token']
        # Twitch PubSub endpoint
        self.uri = credentials['server']
        # Elevenlabs api
        self.elevenlabs_api = elevenlabs_api

    async def listen(self):
        async with websockets.connect(self.uri) as websocket:
            # Send a message to the server to listen to a specific topic
            await websocket.send(json.dumps({
                "type": "LISTEN",
                "data": {
                    "topics": self.topics,
                    "auth_token": self.auth_token
                }
            }))
            print("Connection with twitch chat established, reading rewards...")

            while True:
                response = await websocket.recv()
                data = json.loads(response)
                await websocket.send(json.dumps({"type": "PING"}))

                # Process the received data
                if data["type"] == "MESSAGE":
                    # because twitch apparently never heard of a dict, we have to make it into json format
                    message = json.loads(data['data']['message'])

                    # seriously twitch?
                    reward_type = message['data']['redemption']['reward']['title']
                    username = message['data']['redemption']['user']['display_name']

                    if reward_type == 'Talk through Thilda':
                        user_input = message['data']['redemption']['user_input']
                        # retrieve raw audio bytes
                        tts = self.elevenlabs_api.get_text_to_speech(
                            text_to_convert=user_input,
                            voice_id="YEKqplDYDAEDfyy3K3ZX")

                        # TODO: make bad word filter

                        # read out raw bytes and play in real time
                        play_audio(tts)

                    # todo: logic of executing tts and making thilda appear in obs
