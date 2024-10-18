import pyaudio


class DeviceManager:
    def __init__(self):
        self.audio = pyaudio.PyAudio()

    def get_microphone_devices(self):
        device_count = self.audio.get_device_count()
        microphone_devices = []
        for i in range(device_count):
            device_info = self.audio.get_device_info_by_index(i)
            if device_info["maxInputChannels"] > 0:  # Input device
                microphone_devices.append(
                    {
                        "index": i,
                        "name": device_info["name"],
                    }
                )
        return microphone_devices

    def get_output_devices(self):
        device_count = self.audio.get_device_count()
        output_devices = []
        for i in range(device_count):
            device_info = self.audio.get_device_info_by_index(i)
            if device_info["maxOutputChannels"] > 0:  # Output device
                output_devices.append(
                    {
                        "index": i,
                        "name": device_info["name"],
                    }
                )
        return output_devices
