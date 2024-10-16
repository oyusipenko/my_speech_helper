import time
import json
from PyQt5.QtCore import QThread, pyqtSignal


class RecognitionThread(QThread):
    text_received = pyqtSignal(str)

    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.running = True

    def run(self):
        print("RecognitionThread started")
        while self.running:
            if self.manager.stream is None:
                time.sleep(0.1)
                continue

            try:
                data = self.manager.stream.read(4096, exception_on_overflow=False)
                if len(data) == 0:
                    continue

                if self.manager.recognizer.AcceptWaveform(data):
                    result = self.manager.recognizer.Result()
                    text = json.loads(result).get("text", "")
                    if text:
                        print(f"Recognized: {text}")
                        self.text_received.emit(text)
                else:
                    partial_result = self.manager.recognizer.PartialResult()
                    partial_text = json.loads(partial_result).get("partial", "")
                    if partial_text:
                        print(f"Partial: {partial_text}")

                time.sleep(0.01)

            except OSError as e:
                print(f"Audio stream read error: {e}")
                continue

    def stop(self):

        self.running = False
        self.quit()
        self.wait()
        print("RecognitionThread stopped")
