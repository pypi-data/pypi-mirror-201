"""
Module for start messages 

:author: Julian M. Kleber
"""

from click import echo

from lia.conversation.emojis import (
    mechanical_arm,
    call_me_hand,
    sailing_ship,
    anatomical_heart,
)


def say_start_message() -> None:
    """
    The say_start_message function prints a message to the console that welcomes the user and
    explains how to use this program.

    :return: None

    :doc-author: Julian M. Kleber
    """

    message = standard_message()
    echo(message=message)


def standard_message() -> str:
    """
    The standard_message function returns a string that is the standard message
    that Lia prints to the console when it starts up.

    :return: A string.

    :doc-author: Julian M. Kleber
    """

    message = (
        f"{anatomical_heart} Lia is an open-source CI/CD tool\n"
        f"that eliminates the Fel {mechanical_arm}\n"
        f"Copyright © 2023 Soul Twin Studios {call_me_hand}\n"
        f"A subsidiary of SailBlack Inc. {sailing_ship}"
    )
    return message
