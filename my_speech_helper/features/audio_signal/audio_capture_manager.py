import pyaudio
import numpy as np


class AudioCaptureManager:
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.stream_me = None
        self.stream_interviewer = None

    def get_supported_sample_rate(self, device_index):
        supported_rates = [
            44100,
            48000,
            32000,
            16000,
            8000,
        ]
        for rate in supported_rates:
            try:
                self.audio.is_format_supported(
                    rate,
                    input_device=device_index,
                    input_channels=1,
                    input_format=pyaudio.paFloat32,
                )
                print(f"Supported sample rate found: {rate}")
                return rate
            except ValueError:
                continue
        raise ValueError("No supported sample rates found for the device")

    def start_signal_check(self, device_index_me, device_index_interviewer):
        print(
            f"Starting signal check on devices: Microphone Index {device_index_me}, Desktop Audio Index {device_index_interviewer}"
        )

        try:
            sample_rate_me = self.get_supported_sample_rate(device_index_me)

            self.stream_me = self.audio.open(
                format=pyaudio.paFloat32,
                channels=1,
                rate=sample_rate_me,
                input=True,
                input_device_index=device_index_me,
                frames_per_buffer=2048,
            )  # Increased buffer size

            print(f"self.stream_me {self.stream_me}")
            # if device_index_interviewer is not None:
            #     # Get the supported sample rate for the desktop audio device (if available)
            #     sample_rate_interviewer = self.get_supported_sample_rate(
            #         device_index_interviewer
            #     )
            #
            #     self.stream_interviewer = self.audio.open(
            #         format=pyaudio.paFloat32,
            #         channels=1,
            #         rate=sample_rate_interviewer,
            #         input=True,
            #         input_device_index=device_index_interviewer,
            #         frames_per_buffer=2048,
            #     )
            # else:
            #     print("No desktop audio device found.")
        except Exception as e:
            print(f"Error starting the stream: {e}")

    def stop_signal_check(self):
        """Stop the audio signal check."""
        if self.stream_me:
            self.stream_me.stop_stream()
            self.stream_me.close()
        if self.stream_interviewer:
            self.stream_interviewer.stop_stream()
            self.stream_interviewer.close()
        print("Signal check stopped.")

    def check_audio_levels(self):
        audio_level_me = 0
        audio_level_interviewer = 0

        try:
            if self.stream_me:
                audio_data_me = np.frombuffer(
                    self.stream_me.read(2048, exception_on_overflow=False),
                    dtype=np.float32,
                )
                print(f"check_audio_levels 2222, {np.abs(audio_data_me).mean()}")
                audio_level_me = np.abs(audio_data_me).mean()

            # if self.stream_interviewer:
            #     audio_data_interviewer = np.frombuffer(
            #         self.stream_interviewer.read(2048, exception_on_overflow=False),
            #         dtype=np.float32,
            #     )
            #     audio_level_interviewer = np.abs(audio_data_interviewer).mean()

        except Exception as e:
            print(f"Error checking audio levels: {e}")
        return audio_level_me, audio_level_interviewer

    def terminate(self):
        self.audio.terminate()
