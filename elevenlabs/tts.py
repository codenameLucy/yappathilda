import io

import soundfile as sf
import sounddevice as sd


class RawAudioException(Exception):
    pass


def play_audio(raw_audio: bytes, audio_device: str):
    try:
        sd.default.device = audio_device
        sd.play(*sf.read(io.BytesIO(raw_audio)))
        sd.wait()
    except Exception as e:
        raise RawAudioException(f"exception occurred during attempt at playing raw audio bytes: {e}") from e
