from PyQt5.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QComboBox,
    QLabel,
    QTextEdit,
)

from my_speech_helper.features.audio_signal.controller import AudioSignalController
from my_speech_helper.features.speech_recognition.controller import (
    SpeechRecognitionController,
)
from my_speech_helper.utils.state_manager import state_manager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.audio_controller = AudioSignalController()
        self.speech_recognition_controller = SpeechRecognitionController()
        self.setup_ui()
        self.setWindowTitle("Interview Helper")
        self.setGeometry(100, 100, 800, 600)

        state_manager.state_changed.connect(self.update_recognized_text_display)

    def setup_ui(self):
        self.microphone_devices = self.audio_controller.get_microphone_devices()
        self.output_label_me = QLabel("Select your microphone:")
        self.output_combo_me = QComboBox()
        self.output_combo_me.addItems(
            [device["name"] for device in self.microphone_devices]
        )
        self.audio_controller.handle_change_device_me(
            self.microphone_devices[0]["name"]
        )
        self.output_combo_me.currentTextChanged.connect(
            self.audio_controller.handle_change_device_me
        )

        self.audio_activity_me = QLabel("Your microphone signal: no signal")
        self.recognized_text_display = QTextEdit()
        self.recognized_text_display.setReadOnly(True)
        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")
        self.start_button.clicked.connect(self.on_start_clicked)
        self.stop_button.clicked.connect(self.on_stop_clicked)

        layout = QVBoxLayout()
        layout.addWidget(self.output_label_me)
        layout.addWidget(self.output_combo_me)
        layout.addWidget(self.audio_activity_me)
        layout.addWidget(self.recognized_text_display)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def on_start_clicked(self):
        self.speech_recognition_controller.start_recognition()

    def on_stop_clicked(self):
        self.speech_recognition_controller.stop_recognition()

    def update_recognized_text_display(self, state):
        recognized_texts = state["text_output"]["user"]
        display_text = ""
        for entry in recognized_texts:
            display_text += f"User({entry['date']}): \"{entry['text']}\"\n"
        self.recognized_text_display.setPlainText(display_text)
