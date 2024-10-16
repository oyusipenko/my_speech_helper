from PyQt5.QtCore import QObject, pyqtSignal


class StateManager(QObject):
    state_changed = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self._state = {
            "user_microphone": {
                "selected_microphone": {
                    "index": None,
                    "name": None,
                },
                "audio_level": 0.0,
            },
            "desktop_audio": {
                "audio_level": 0.0,
            },
            "text_output": {
                "user": [{"date": "2024-10-15", "text": "Test User Text"}],
                "desktop": [{"date": "2024-10-16", "text": "Test Desktop Text"}],
                "open_ai": [{"date": "2024-10-17", "text": "Test Open AI Text"}],
            },
        }

    def get_state(self, key=None):
        if key:
            return self._state.get(key, None)
        return self._state

    def set_state(self, key, value):
        self._state[key] = value
        self.state_changed.emit(self._state)


state_manager = StateManager()
