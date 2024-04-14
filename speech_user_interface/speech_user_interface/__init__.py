from dotenv import load_dotenv
from typing import Callable, NoReturn
from openai import OpenAI
import os
import copy

from .read_in_speech import read_in_speech
from .send_text_to_chatgpt import send_text_to_chatgpt
from .speak_text import speak_text
from .compare_strings import compare_strings
from .CommandResults import CommandResults
from .CommandArgs import CommandArgs
from .build_probabilities_for_speech import build_probabilities_for_speech


__name__ == "__main__"
__all__ = [
    "compare_strings",
    "read_in_speech",
    "send_text_to_chatgpt",
    "speak_text",
]


def run_function_on_chatgpt(args: CommandArgs) -> CommandResults:
    newArgs = copy.deepcopy(args)
    newArgs.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    reponse_text = send_text_to_chatgpt(newArgs)
    speak_text(reponse_text)

    return CommandResults(False)


def exit_program(args: CommandArgs) -> CommandResults:
    exit()

    return CommandResults(true)


greeting = "The program is ready for you to begin speaking..."
# we make a mapping from commands to functions and run the function
# if we fuzzy detect a match to the command as the input
run_function_on_command: dict[str, Callable[[CommandArgs], CommandResults]] = {
    "chat GPT": run_function_on_chatgpt,
    "chat g p t": run_function_on_chatgpt,
    "exit the program": exit_program,
    "exit program": exit_program,
}


def set_extra_commands(
    extra_commands: dict[str, Callable[[CommandArgs], CommandResults]]
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
) -> NoReturn:
    prep_function()
    # read in speech from the user as a sound file
    # process that speech and convert it to text

    # Inform user to start speaking
    speak_text(greeting)
    command_results: tuple[
        CommandResults, Callable[[CommandArgs], CommandResults] | None
    ] = (CommandResults(True), None)
    while True:
        already_ran_command = False
        speech_text = read_in_speech()
        print("read in speech_text:", speech_text)
        command_speech_probabilities = build_probabilities_for_speech(
            speech_text, run_function_on_command
        )
        for _, (
            command_func,
            command_prob,
        ) in command_speech_probabilities.items():
            if command_prob > 0.8:
                command_results = (
                    command_func(CommandArgs(speech_text)),
                    command_func,
                )
                already_ran_command = True
                break

        if (
            not already_ran_command
            and command_results[1]
            and not command_results[0].exit_on_done
        ):
            command_results = (
                command_results[1](CommandArgs(speech_text)),
                command_results[1],
            )

    # use the text to talk to ChatGPT
    # take ChatGPT's response and convert that to speech


def main(
    prep_function=default_prep_function,
):
    speech_user_interface(prep_function)
