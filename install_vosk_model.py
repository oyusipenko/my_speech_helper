import os
import urllib.request
import zipfile


VOSK_MODEL_URL = (
    "https://alphacephei.com/vosk/models/vosk-model-en-us-0.42-gigaspeech.zip"
)
VOSK_MODEL_DIR = "./models/vosk-model-en-us-0.42-gigaspeech"


def download_progress_hook(block_num, block_size, total_size):
    downloaded = block_num * block_size
    progress_percentage = 100 * downloaded / total_size
    total_mb = total_size / (1024 * 1024)
    downloaded_mb = downloaded / (1024 * 1024)

    if downloaded < total_size:
        print(
            f"Downloading: {progress_percentage:.2f}% | {downloaded_mb:.2f} MB / {total_mb:.2f} MB",
            end="\r",
        )
    else:
        print(f"Download complete: 100% | {total_mb:.2f} MB / {total_mb:.2f} MB")


def download_and_extract_model():
    if not os.path.exists(VOSK_MODEL_DIR):
        print(f"Downloading Vosk model from {VOSK_MODEL_URL}...")

        os.makedirs("./models", exist_ok=True)

        model_zip_path = "./models/vosk-model.zip"

        urllib.request.urlretrieve(
            VOSK_MODEL_URL, filename=model_zip_path, reporthook=download_progress_hook
        )

        print("\nExtracting model...")
        with zipfile.ZipFile(model_zip_path, mode="r") as zip_ref:
            zip_ref.extractall("./models")

        print(f"Model downloaded and extracted to {VOSK_MODEL_DIR}")

        os.remove(model_zip_path)
    else:
        print(f"Model already exists at {VOSK_MODEL_DIR}")


if __name__ == "__main__":
    download_and_extract_model()
