import pyaudio


class DeviceManager:
    def __init__(self):
        self.audio = pyaudio.PyAudio()

    def get_desktop_audio_device(self):
        audio = pyaudio.PyAudio()

        for i in range(audio.get_device_count()):
            device_info = audio.get_device_info_by_index(i)

            if (
                "Stereo Mix" in device_info["name"]
                or "loopback" in device_info["name"].lower()
            ):

                return {
                    "index": i,
                    "name": device_info["name"],
                    "type": "Desktop Audio",
                }

        audio.terminate()
        print("No desktop audio device found (loopback or Stereo Mix)")
        return None

    def get_microphone_devices(self):
        audio = pyaudio.PyAudio()
        devices = []

        for i in range(audio.get_device_count()):
            device_info = audio.get_device_info_by_index(i)

            if device_info["maxInputChannels"] > 0:
                devices.append(
                    {"index": i, "name": device_info["name"], "type": "Input"}
                )

        audio.terminate()
        if not devices:
            print("No microphone devices found.")
        return devices

    def terminate(self):
        self.audio.terminate()
