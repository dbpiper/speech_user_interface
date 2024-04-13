from dotenv import load_dotenv
import os

from .read_in_speech import read_in_speech
from .send_text_to_chatgpt import send_text_to_chatgpt
from .speak_text import speak_text
from .compare_strings import compare_strings
from .load_vosk_model import load_vosk_model


__name__ == "__main__"
__all__ = []


def main():
    load_dotenv()
    vosk_model = load_vosk_model()
    # read in speech from the user as a sound file
    # process that speech and convert it to text

    # Inform user to start speaking
    speak_text("The program is ready for you to begin speaking...")
    if vosk_model:
        while True:
            speech_text = read_in_speech(vosk_model)
            if isinstance(speech_text, str):
                print(
                    'compare_strings(speech_text, "exit the program"):',
                    compare_strings(speech_text, "exit the program"),
                )
                if compare_strings(speech_text, "exit the program") > 0.6:
                    break

                print("speech_text:", speech_text)
                reponse_text = send_text_to_chatgpt(speech_text)
                speak_text(reponse_text)

    # use the text to talk to ChatGPT
    # take ChatGPT's response and convert that to speech
