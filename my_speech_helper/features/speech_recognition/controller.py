from my_speech_helper.features.speech_recognition.speech_recognition_manager import (
    SpeechRecognitionManager,
)


class SpeechRecognitionController:
    def __init__(self):
        self.speech_manager = SpeechRecognitionManager()

    def start_recognition(self):
        self.speech_manager.start_stream()
        self.speech_manager.start_recognition_thread()

    def stop_recognition(self):
        self.speech_manager.stop_recognition()
        self.speech_manager.terminate()
