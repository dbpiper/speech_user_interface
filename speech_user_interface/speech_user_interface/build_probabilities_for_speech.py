from typing import Callable

from .CommandResults import CommandResults
from .compare_strings import compare_strings


def build_probabilities_for_speech(
    speech_text: str, commands: dict[str, Callable[[str], CommandResults]]
) -> dict[str, tuple[Callable[[str], CommandResults], float]]:
    probabilities: dict[str, tuple[Callable[[str], CommandResults], float]] = (
        dict()
    )

    for command in commands:
        probabilities[command] = (
            commands[command],
            compare_strings(speech_text, command),
        )

    return probabilities
