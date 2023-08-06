"""
Module for exit messages.

:author: Julian M. Kleber
"""
from click import echo

from lia.conversation.start_message import standard_message


def say_end_message() -> None:
    """Goodbye message."""

    message = (
        "Thank you for using Lia.\n"
        + standard_message()
        + "For more nice things follow us on www.codeberg.org/sail.black"
    )
    echo(message=message)
