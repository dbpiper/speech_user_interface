from dataclasses import dataclass


@dataclass
class CommandResults:
    """Class for keeping track of a command's args."""

    exit_on_done: bool
