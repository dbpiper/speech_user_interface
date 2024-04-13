from dotenv import load_dotenv

from .read_in_speech import read_in_speech
from .send_text_to_chatgpt import send_text_to_chatgpt
from .speak_text import speak_text
from .compare_strings import compare_strings
from .load_vosk_model import load_vosk_model


__name__ == "__main__"
__all__ = [
    "speak_text",
    "send_text_to_chatgpt",
    "compare_strings",
    "read_in_speech",
    "load_vosk_model",
]

exit_string = ""
greeting = ""
# expose a function to run when the app is


def default_function_to_run(input_text: str):
    reponse_text = send_text_to_chatgpt(input_text)
    speak_text(reponse_text)


def default_prep_function():
    load_dotenv()


def set_exit_string():
    global exit_string
    exit_string = "exit the program"


def set_greeting():
    global greeting
    greeting = "The program is ready for you to begin speaking..."


def speech_user_interface(
    prep_function=default_prep_function,
    function_to_run=default_function_to_run,
):
    prep_function()
    vosk_model = load_vosk_model()
    # read in speech from the user as a sound file
    # process that speech and convert it to text

    # Inform user to start speaking
    set_exit_string()
    speak_text(greeting)
    if vosk_model:
        while True:
            speech_text = read_in_speech(vosk_model)
            if isinstance(speech_text, str):
                if compare_strings(speech_text, exit_string) > 0.5:
                    break

                function_to_run(speech_text)

    # use the text to talk to ChatGPT
    # take ChatGPT's response and convert that to speech


def main(
    prep_function=default_prep_function,
    function_to_run=default_function_to_run,
):
    speech_user_interface(prep_function, function_to_run)
