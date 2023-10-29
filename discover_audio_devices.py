import pyaudio

def list_audio_output_devices():
    audio = pyaudio.PyAudio()
    device_count = audio.get_device_count()

    print("Available audio output devices:")

    for i in range(device_count):
        device_info = audio.get_device_info_by_index(i)
        if device_info['maxOutputChannels'] > 0:
            print(f"{i}: {device_info['name']}")

    audio.terminate()

if __name__ == "__main__":
    list_audio_output_devices()