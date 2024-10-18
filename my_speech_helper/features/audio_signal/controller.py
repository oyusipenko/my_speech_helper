from my_speech_helper.features.audio_signal.device_manager import DeviceManager
from my_speech_helper.utils.state_manager import state_manager


class AudioSignalController:
    def __init__(self):
        self.device_manager = DeviceManager()

    def get_microphone_devices(self):
        return self.device_manager.get_microphone_devices()

    def get_output_devices(self):
        return self.device_manager.get_output_devices()

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
            print("No such microphone found.")

        prev_state = state_manager.get_state("user_microphone") or {}
        new_state = {
            **prev_state,
            "selected_microphone": {
                "index": selected_device["index"],
                "name": selected_device["name"],
            },
        }
        state_manager.set_state("user_microphone", new_state)

    def handle_change_device_interviewer(self, device_interviewer_name):
        selected_device = next(
            (
                device
                for device in self.get_output_devices()
                if device["name"] == device_interviewer_name
            ),
            None,
        )

        if selected_device is None:
            print("No such output device found.")

        prev_state = state_manager.get_state("desktop_audio") or {}
        new_state = {
            **prev_state,
            "selected_desktop_audio": {
                "index": selected_device["index"],
                "name": selected_device["name"],
            },
        }
        state_manager.set_state("desktop_audio", new_state)
        print(f"handle_change_device_interviewer STATE {state_manager.get_state()}")
