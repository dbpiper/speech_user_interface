from dotenv import load_dotenv
from typing import Callable, cast
from dataclasses import dataclass

from .read_in_speech import read_in_speech
from .send_text_to_chatgpt import send_text_to_chatgpt
from .speak_text import speak_text
from .compare_strings import compare_strings


__name__ == "__main__"
__all__ = [
    "compare_strings",
    "read_in_speech",
    "send_text_to_chatgpt",
    "speak_text",
]


@dataclass
class CommandResults:
    """Class for keeping track of a command's args."""

    exit_on_done: bool


def run_function_on_chatgpt(input_text: str) -> CommandResults:
    reponse_text = send_text_to_chatgpt(input_text)
    speak_text(reponse_text)

    return CommandResults(False)


def exit_program(input_text: str) -> CommandResults:
    exit()

    return CommandResults(true)


greeting = "The program is ready for you to begin speaking..."
# we make a mapping from commands to functions and run the function
# if we fuzzy detect a match to the command as the input
run_function_on_command: dict[str, Callable[[str], CommandResults]] = {
    "chat GPT": run_function_on_chatgpt,
    "exit the program": exit_program,
}


def set_extra_commands(
    extra_commands: dict[str, Callable[[str], CommandResults]]
):
    global run_function_on_command
    for extra_command, command_func in extra_commands.items():
        run_function_on_command[extra_command] = command_func


def default_prep_function():
    load_dotenv()


def set_greeting(new_greeting: str):
    global greeting
    greeting = new_greeting


def speech_user_interface(
    prep_function=default_prep_function,
):
    prep_function()
    # read in speech from the user as a sound file
    # process that speech and convert it to text

    # Inform user to start speaking
    speak_text(greeting)
    while True:
        speech_text = read_in_speech()
        print("read in speech_text:", speech_text)
        command_results = CommandResults(True)

        for command, command_func in run_function_on_command.items():
            while not command_results.exit_on_done:
                if isinstance(speech_text, str):
                    print(
                        f"""compare_strings(speech_text, command):
                        {compare_strings(speech_text, command)}
                        speech_text:{speech_text}
                        command:{command}
                        """,
                        compare_strings(speech_text, command),
                    )
                    if compare_strings(speech_text, command) > 0.9:
                        speech_text = read_in_speech()
                        if isinstance(speech_text, str):
                            command_results = command_func(speech_text)

    # use the text to talk to ChatGPT
    # take ChatGPT's response and convert that to speech


def main(
    prep_function=default_prep_function,
):
    speech_user_interface(prep_function)
