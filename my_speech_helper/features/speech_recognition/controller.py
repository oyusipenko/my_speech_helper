from datetime import datetime
from my_speech_helper.features.speech_recognition.recognition_thread import (
    RecognitionThread,
)
from my_speech_helper.features.speech_recognition.speech_recognition_manager import (
    SpeechRecognitionManager,
)
from my_speech_helper.utils.state_manager import state_manager


class SpeechRecognitionController:
    def __init__(self):
        self.speech_manager_me = SpeechRecognitionManager()
        self.speech_manager_interviewer = SpeechRecognitionManager()
        self.recognition_thread_me = None
        self.recognition_thread_interviewer = None

    def start_recognition(self):
        # Start recognition for the user (microphone)
        self.speech_manager_me.start_stream("user_microphone")
        self.recognition_thread_me = RecognitionThread(
            self.speech_manager_me, "user_microphone"
        )
        self.recognition_thread_me.text_received.connect(
            self.update_state_with_recognized_text_me
        )
        self.recognition_thread_me.start()

        # Start recognition for the desktop audio (use default system audio output)
        self.speech_manager_interviewer.start_stream("desktop_output")
        self.recognition_thread_interviewer = RecognitionThread(
            self.speech_manager_interviewer, "desktop_output"
        )
        self.recognition_thread_interviewer.text_received.connect(
            self.update_state_with_recognized_text_interviewer
        )
        self.recognition_thread_interviewer.start()

    def stop_recognition(self):
        if self.recognition_thread_me:
            self.recognition_thread_me.stop()
        if self.recognition_thread_interviewer:
            self.recognition_thread_interviewer.stop()

        self.speech_manager_me.stop_stream("user_microphone")
        self.speech_manager_interviewer.stop_stream("desktop_output")

    def update_state_with_recognized_text_me(self, text):
        # Update state for user microphone
        prev_state = state_manager.get_state()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_entry = {"date": current_time, "text": text}
        updated_user_text = prev_state["text_output"].get("user", []) + [new_entry]
        new_state = prev_state.copy()
        new_state["text_output"]["user"] = updated_user_text
        state_manager.set_state("text_output", new_state["text_output"])
        print(f"State updated with new recognized text from user: {new_entry}")

    def update_state_with_recognized_text_interviewer(self, text):
        # Update state for desktop output
        prev_state = state_manager.get_state()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_entry = {"date": current_time, "text": text}
        updated_interviewer_text = prev_state["text_output"].get("interviewer", []) + [
            new_entry
        ]
        new_state = prev_state.copy()
        new_state["text_output"]["interviewer"] = updated_interviewer_text
        state_manager.set_state("text_output", new_state["text_output"])
        print(f"State updated with new recognized text from interviewer: {new_entry}")
