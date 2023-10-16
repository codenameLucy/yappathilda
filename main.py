from elevenlabs.elevenlabs_api import ElevenLabsAPI
from elevenlabs.tts import play_audio

if __name__ == '__main__':

    elevenlabs_api = ElevenLabsAPI("b295d3a1d4b6ad97798ed8deda6a2fa1")
    get_voice = elevenlabs_api.get_voice(voice_id="YEKqplDYDAEDfyy3K3ZX")

    # retrieve raw audio bytes
    tts = elevenlabs_api.get_text_to_speech(text_to_convert="This is a test sentence", voice_id="YEKqplDYDAEDfyy3K3ZX")

    # read out raw bytes and play in real time
    play_audio(tts)

