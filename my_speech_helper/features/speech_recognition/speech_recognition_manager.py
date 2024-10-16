import vosk
import pyaudio
import os
from datetime import datetime

from my_speech_helper.features.speech_recognition.recognition_thread import (
    RecognitionThread,
)
from my_speech_helper.utils.state_manager import state_manager


class SpeechRecognitionManager:
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.model = self.load_vosk_model()
        self.recognizer = None
        self.recognition_thread = None

    def load_vosk_model(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.abspath(
            os.path.join(
                current_dir, "../../../models/vosk-model-en-us-0.42-gigaspeech"
            )
        )
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Vosk model not found at: {model_path}")

        print(f"Loaded Vosk model from {model_path}")
        return vosk.Model(model_path)

    def start_stream(self):
        device_index = (
            state_manager.get_state()["user_microphone"]["selected_microphone"]["index"]
            or None
        )
        try:
            print(f"Initializing stream... device_index: {device_index}")
            self.stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=int(
                    self.audio.get_device_info_by_index(device_index)[
                        "defaultSampleRate"
                    ]
                ),
                input=True,
                input_device_index=device_index,
                frames_per_buffer=4096,
            )
            self.stream.start_stream()
            print("Stream successfully started")

            self.recognizer = vosk.KaldiRecognizer(
                self.model,
                int(
                    self.audio.get_device_info_by_index(device_index)[
                        "defaultSampleRate"
                    ]
                ),
            )
        except Exception as e:
            print(f"Failed to start stream: {e}")

    def stop_stream(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        print("Stream stopped")

    def start_recognition_thread(self):
        self.recognition_thread = RecognitionThread(self)
        self.recognition_thread.text_received.connect(
            self.update_state_with_recognized_text
        )
        self.recognition_thread.start()

    def stop_recognition(self):
        if self.recognition_thread:
            self.recognition_thread.stop()
        self.stop_stream()

    def update_state_with_recognized_text(self, text):
        prev_state = state_manager.get_state()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_entry = {"date": current_time, "text": text}
        updated_user_text = prev_state["text_output"]["user"] + [new_entry]
        new_state = prev_state.copy()
        new_state["text_output"]["user"] = updated_user_text
        state_manager.set_state("text_output", new_state["text_output"])
        print(f"State updated with new recognized text: {new_entry}")

    def terminate(self):
        self.audio.terminate()
        print("Audio system terminated")
