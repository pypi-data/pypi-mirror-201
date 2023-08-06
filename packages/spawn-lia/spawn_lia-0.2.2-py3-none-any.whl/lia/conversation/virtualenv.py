"""
Conversation about the virtualenv method

:author: Julian M. Kleber
"""

import sys
import subprocess
from click import echo
from amarium.utils import append_slash

from lia.conversation.emojis import (
    face_with_rolling_eyes,
    kissing_cat,
    magic_wand,
    pointing_down,
    broken_heart,
    dizzy,
    pensive_face,
)


def is_activated(venv_path: str) -> str:
    """
    The is_activated function checks if a virtualenv is already activated.
    If so, it returns a message with the path to the venv.

    :param venv_path:str: Used to pass the path of the venv to be deactivated.
    :return: The message for the CLI tool.

    :doc-author: Julian M. Kleber
    """

    message = (
        f"\n{broken_heart}{broken_heart}{broken_heart}\n"
        f"Oh, no! You have already a virtualenv activated {face_with_rolling_eyes}\n"
        f"I recommend to deactivate the running virtualenv {kissing_cat}{magic_wand}\n"
        f"{pointing_down}The venv is in{pointing_down}\n\n"
        f"{venv_path}"
    )
    return message


def shall_i_deactivate(
    venv_path: str,
) -> (
    None
):  # TODO: Experimental feature -> handling the shells a bit difficult, deactivate must be run
    # in the same shell
    """
    The shall_i_deactivate function asks the user if they want to deactivate their virtualenv.
        If the answer is 'y', then it will run a subprocess that runs "deactivate" in the shell.
        If not, it will exit with an error message.

    :return: None.

    :doc-author: Julian M. Kleber
    """

    venv_path = append_slash(venv_path) + "bin/activate"

    answer = input("Shall I deactivate the virtualenv for you? (y/n)\n")
    answer = answer.lower()

    if answer == "n":
        echo(f"Okay, I guess you got this... {pensive_face}")
    elif answer == "y":
        echo(f"Good decision, darling {magic_wand} {kissing_cat}")
        out = subprocess.run(
            ["source", venv_path, "&&", "deactivate"],
            check=True,
            shell=True,
            capture_output=True,
        )
        echo(f"Okay, I am done {dizzy}")
        sys.exit()
    else:
        echo(f"You have to decide y/n, darling...{face_with_rolling_eyes}")
        sys.exit()
