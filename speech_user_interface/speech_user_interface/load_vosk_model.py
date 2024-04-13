import os
from vosk import Model

from .CONSTANTS import VOSK_MODEL_PATH
from .download_file import download_file
from .unzip_file import unzip_file
from .move_directory_up_one_level import move_directory_up_one_level


def load_vosk_model():
    # Resolve the model path
    model_path = os.path.abspath(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..",
            VOSK_MODEL_PATH,
        )
    )

    # Check if the model path exists
    try:
        return Model(model_path)
    except Exception:
        zip_path = f"{model_path}.zip"
        if not os.path.exists(zip_path):
            download_file(
                "https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip",
                zip_path,
            )
        unzip_file(zip_path, model_path)
        model_path = os.path.join(model_path, "vosk-model-en-us-0.22")
        print("os.listdir(model_path):", os.listdir(model_path))

    # Load the Vosk model
    return Model(model_path)
