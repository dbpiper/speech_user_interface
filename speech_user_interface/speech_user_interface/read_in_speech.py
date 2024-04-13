import os
import sys
import pyaudio
from vosk import Model, KaldiRecognizer

from .CONSTANTS import VOSK_MODEL_PATH
from .speak_text import speak_text


def read_in_speech(vosk_model: Model, threshold=500, silence_duration=3):
    # Convert silence duration to the number of frames
    silence_limit = int(
        silence_duration * 16000 / 8192
    )  # sample rate / frames_per_buffer

    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Open audio stream
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=8192,
    )
    stream.start_stream()

    # Create a recognizer with the model
    recognizer = KaldiRecognizer(vosk_model, 16000)

    while True:
        data = stream.read(8192, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            # Check for final, confirmed result
            if result:
                print("Final result:", result)
                break  # Exit loop on confirmed result
        else:
            print(
                "Listening..."
            )  # Optionally, show message indicating listening status

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    return result


# Adjust the threshold and silence duration based on testing with your specific environment.
