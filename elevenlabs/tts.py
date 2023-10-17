import io

import soundfile as sf
import sounddevice as sd


def play_audio(raw_audio: bytes):
    try:
        sd.default.device = 'Headphones (3- Shure MV7), MME'
        sd.play(*sf.read(io.BytesIO(raw_audio)))
        sd.wait()
    except Exception as e:
        return print(f"exception occured during attempt at playing raw audio bytes: {e}")

