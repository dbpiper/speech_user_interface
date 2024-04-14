from typing import Callable

from .CommandResults import CommandResults
from .CommandArgs import CommandArgs
from .compare_strings import compare_strings


def build_probabilities_for_speech(
    speech_text: str,
    commands: dict[str, Callable[[CommandArgs], CommandResults]],
) -> dict[str, tuple[Callable[[CommandArgs], CommandResults], float]]:
    probabilities: dict[
        str, tuple[Callable[[CommandArgs], CommandResults], float]
    ] = dict()

    for command in commands:
        probabilities[command] = (
            commands[command],
            compare_strings(speech_text, command),
        )

    return probabilities
