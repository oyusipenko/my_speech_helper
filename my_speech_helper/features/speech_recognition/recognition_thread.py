import time
import json
from PyQt5.QtCore import QThread, pyqtSignal


class RecognitionThread(QThread):
    text_received = pyqtSignal(str)

    def __init__(self, manager, stream_type):
        super().__init__()
        self.manager = manager
        self.stream_type = stream_type
        self.running = True

    def run(self):
        print(f"RecognitionThread started for {self.stream_type}")
        while self.running:
            stream = self.manager.streams.get(self.stream_type, None)
            if stream is None:
                time.sleep(0.1)
                continue

            try:
                data = stream.read(4096, exception_on_overflow=False)
                if len(data) == 0:
                    continue

                recognizer = self.manager.recognizers[self.stream_type]

                if recognizer.AcceptWaveform(data):
                    result = recognizer.Result()
                    text = json.loads(result).get("text", "")
                    if text:
                        print(f"Recognized on {self.stream_type}: {text}")
                        self.text_received.emit(text)
                else:
                    partial_result = recognizer.PartialResult()
                    partial_text = json.loads(partial_result).get("partial", "")
                    if partial_text:
                        print(f"Partial on {self.stream_type}: {partial_text}")

                time.sleep(0.01)

            except OSError as e:
                print(f"Audio stream read error on {self.stream_type}: {e}")
                continue

    def stop(self):
        self.running = False
        self.quit()
        self.wait()
        print(f"RecognitionThread stopped for {self.stream_type}")
