import sounddevice as sd


def list_audio_devices():
    audio_devices = sd.query_devices()

    print("Available audio devices:")
    for i, device in enumerate(audio_devices):
        print(f"{i + 1}. {device['name']} (Device ID: {device['name']})")


if __name__ == "__main__":
    list_audio_devices()
    input("press enter to close program (Please make sure to use DEVICE ID)")
