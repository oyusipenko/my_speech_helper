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
            },
            "desktop_audio": {
                "selected_desktop_audio": {
                    "index": None,
                    "name": None,
                },
            },
            "text_output": {
                "user": [],
                "interviewer": [],
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
