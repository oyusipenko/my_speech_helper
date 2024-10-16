from my_speech_helper.features.audio_signal.audio_capture_manager import (
    AudioCaptureManager,
)
from my_speech_helper.features.audio_signal.device_manager import DeviceManager
from my_speech_helper.utils.state_manager import state_manager


class AudioSignalController:
    def __init__(self):
        self.audio_manager = AudioCaptureManager()
        self.device_manager = DeviceManager()
        print(f"test {state_manager.get_state()}")

    def start_signal_check(self):
        selected_microphone_index = state_manager.get_state()["user_microphone"][
            "selected_microphone"
        ]["index"]

        return self.audio_manager.start_signal_check(
            device_index_me=selected_microphone_index, device_index_interviewer=0
        )

    def get_microphone_devices(self):
        return self.device_manager.get_microphone_devices()

    def handle_change_device_me(self, device_me_name):

        selected_device = next(
            (
                device
                for device in self.get_microphone_devices()
                if device["name"] == device_me_name
            ),
            None,
        )

        if selected_device is None:
            print("No such device found.")

        prev_state = state_manager.get_state("user_microphone") or {}

        new_state = {
            **prev_state,
            "selected_microphone": {
                "index": selected_device["index"],
                "name": selected_device["name"],
            },
        }

        state_manager.set_state("user_microphone", new_state)
