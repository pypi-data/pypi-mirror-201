"""
The module implements a ask to proceed function

:author: Julian M. Kleber
"""

import sys
from click import echo
from lia.emojis import (
    fearful_face,
    pensive_face,
    magic_wand,
    kissing_cat,
    face_with_rolling_eyes,
)


def ask_to_proceed() -> None:
    """
    The ask_to_proceed function asks the user if they want to proceed with the script.
    If they answer 'y', then it will continue. If they answer 'n', then it will exit.

    :return: None.

    :doc-author: Julian M. Kleber
    """

    answer = input(f"Wouldn't it be better to stop {fearful_face}? (y/n)\n")
    answer = answer.lower()

    if answer == "n":
        echo(f"Okay, I guess you got this... {pensive_face}")
    elif answer == "y":
        echo(f"Good decision, darling {magic_wand} {kissing_cat} ")
        sys.exit()
    else:
        echo(f"You have to decide y/n, darling...{face_with_rolling_eyes}")
        sys.exit()


if __name__ == "__main__":
    ask_to_proceed()
