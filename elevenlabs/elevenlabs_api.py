import requests


class VoiceNotFoundException(Exception):
    pass


class ElevenLabsAPI:
    def __init__(self, json_config: dict):
        self.json_config = json_config
        self.elevenlabs_credentials = self.json_config['elevenlabs_credentials']

        self.api_key = self.elevenlabs_credentials['xi-api-key']
        self.api_url = self.elevenlabs_credentials['api_url']

    def get_voices(self) -> dict:
        headers = {
            'xi-api-key': self.api_key
        }

        voices_url = f"{self.api_url}/v1/voices"
        response = requests.get(voices_url, headers=headers)

        return response.json()

    def get_voice_id(self, voice_name: str) -> int:
        headers = {
            'xi-api-key': self.api_key
        }
        voices = self.get_voices()
        for voice in voices['voices']:
            if voice['name'] == voice_name:
                return voice['voice_id']
        raise VoiceNotFoundException("The given voice name does not match any voices in your library")

    def get_text_to_speech(self, text_to_convert: str, voice_name: str):
        headers = {
            'xi-api-key': self.api_key,
            "optimize_streaming_latency": "0",
            "output_format": "mp3_44100_128"
        }
        request_body = {
            "text": f"{text_to_convert}",
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0,
                "similarity_boost": 0,
                "style": 0,
                "use_speaker_boost": "true"
            }
        }
        voice_id = self.get_voice_id(voice_name=voice_name)

        text_to_speech_url = f"{self.api_url}/v1/text-to-speech/{voice_id}"

        response = requests.post(text_to_speech_url, json=request_body, headers=headers)

        return response.content
