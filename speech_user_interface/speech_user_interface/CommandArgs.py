from dataclasses import dataclass
from openai import OpenAI


@dataclass
class CommandArgs:
    """Class for keeping track of a command's args."""

    text: str = ""
    max_response_length: int = 500
    client: OpenAI | None = None
