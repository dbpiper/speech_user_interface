import os
from vosk import Model

from .CONSTANTS import VOSK_MODEL_PATH
from .speak_text import speak_text


def load_vosk_model():
    # Resolve the model path
    model_path = os.path.abspath(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..",
            VOSK_MODEL_PATH,
        )
    )
    print("Model path:", model_path)

    # Check if the model path exists
    if not os.path.exists(model_path):
        speak_text(
            "Model path does not exist. Please download the model from Vosk."
        )
        return

    # Load the Vosk model
    return Model(model_path)
