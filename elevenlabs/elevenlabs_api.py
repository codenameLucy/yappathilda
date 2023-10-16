import requests


class ElevenLabsAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = "https://api.elevenlabs.io"

    def get_voices(self):
        headers = {
            'xi-api-key': self.api_key
        }

        voices_url = f"{self.api_url}/v1/voices"
        response = requests.get(voices_url, headers=headers)

        return response

    def get_voice(self, voice_id):
        headers = {
            'xi-api-key': self.api_key
        }

        voices_url = f"{self.api_url}/v1/voices/{voice_id}"
        response = requests.get(voices_url, headers=headers)

        return response

    def get_text_to_speech(self, text_to_convert, voice_id):
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
        text_to_speech_url = f"{self.api_url}/v1/text-to-speech/{voice_id}"

        response = requests.post(text_to_speech_url, json=request_body, headers=headers)

        return response.content
