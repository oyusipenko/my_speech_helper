import vosk
import pyaudio
import os

from my_speech_helper.features.audio_signal.controller import AudioSignalController
from my_speech_helper.utils.state_manager import state_manager


class SpeechRecognitionManager:
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.streams = {}
        self.recognizers = {}
        self.models = self.load_vosk_model()
        self.audio_signal_controller = AudioSignalController()

    def load_vosk_model(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.abspath(
            os.path.join(
                current_dir, "../../../models/vosk-model-en-us-0.42-gigaspeech"
            )
        )
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Vosk model not found at: {model_path}")
        return vosk.Model(model_path)

    def start_stream(self, stream_type):
        try:
            if stream_type == "user_microphone":
                device_index = state_manager.get_state()["user_microphone"][
                    "selected_microphone"
                ]["index"]
                print(f"device_info {device_index}")
            else:
                device_index = state_manager.get_state()["desktop_audio"][
                    "selected_desktop_audio"
                ]["index"]
                print(f"device_info {device_index}")

            device_info = self.audio.get_device_info_by_index(device_index)

            channels = int(device_info.get("maxInputChannels", 1))

            print(
                f"Initializing stream for {stream_type}... device_index: {device_index}, channels: {channels}"
            )
            stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=int(device_info["defaultSampleRate"]),
                input=True,
                input_device_index=device_index,
                frames_per_buffer=4096,
            )
            stream.start_stream()
            self.streams[stream_type] = stream

            # Initialize recognizer for the stream
            self.recognizers[stream_type] = vosk.KaldiRecognizer(
                self.models, int(device_info["defaultSampleRate"])
            )
            print(f"Stream for {stream_type} successfully started")

        except Exception as e:
            print(f"Failed to start stream for {stream_type}: {e}")

    def stop_stream(self, stream_type):
        if stream_type in self.streams and self.streams[stream_type]:
            self.streams[stream_type].stop_stream()
            self.streams[stream_type].close()

    def terminate(self):
        self.audio.terminate()
