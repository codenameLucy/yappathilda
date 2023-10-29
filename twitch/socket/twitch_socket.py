import json
import logging
import webbrowser

import websockets

from elevenlabs.elevenlabs_api import ElevenLabsAPI
from elevenlabs.tts import play_audio
from obs.obs_websocket import OBSWebsocket

logger = logging.getLogger(__name__)


class RewardMissingUserInputException(Exception):
    pass


class TwitchRewardSocket:
    def __init__(self, json_config: dict, elevenlabs_api: ElevenLabsAPI):
        self.json_config = json_config
        # Set Twitch credentials
        self.credentials = self.json_config['twitch_credentials']
        channel_id = self.credentials['channel_id']
        self.topics = [f"channel-points-channel-v1.{channel_id}"]
        self.auth_token = self.credentials['auth_token']
        # Twitch PubSub endpoint
        self.uri = self.credentials['server']
        # Elevenlabs
        self.elevenlabs_api = elevenlabs_api
        self.elevenlabs_credentials = self.json_config['elevenlabs_credentials']
        # OBS websocket
        self.obs_ws = OBSWebsocket(obs_credentials=self.json_config['obs_credentials'])

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
            logger.info(" [OK] Connection with twitch chat established, reading rewards...")

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

                    if reward_type == self.credentials['tts_reward_name']:
                        try:
                            user_input = message['data']['redemption']['user_input']
                        except KeyError as e:
                            raise RewardMissingUserInputException(
                                f"Your chosen redeemable reward is missing user input,"
                                f" make sure the reward requires a viewer to enter text. error: {e}") from e

                        # retrieve raw audio bytes
                        tts = self.elevenlabs_api.get_text_to_speech(
                            text_to_convert=user_input,
                            voice_name=self.elevenlabs_credentials["voice_name"])
                        logger.info(f"Audio received with following input: {user_input}")

                        self.obs_ws.change_visibility_tts_scene(visible=True)

                        # read out raw bytes and play in real time
                        play_audio(tts, audio_device=self.elevenlabs_credentials['audio_device'])

                        self.obs_ws.change_visibility_tts_scene(visible=False)
