"""Module that makes Lia to help you avoiding mistakes in git operations.

:author: Julian M. Kleber
"""
import sys
import subprocess
from click import echo
from lia.conversation.emojis import (
    angered_face,
    face_blowing_kiss,
    face_screaming_in_fear,
    magic_wand,
    kissing_cat,
)


from lia.conversation.ask_to_proceed import ask_to_proceed


def verify_branch() -> None:
    """The verify_branch function checks the current branch of the git
    repository. If it is master, then we exit with an error message. If it is
    main, then we ask the user if they want to proceed (and exit if not).
    Otherwise, we assume that everything is fine and continue on our merry way.

    :return: None.

    :doc-author: Julian M. Kleber
    """

    out = subprocess.run(["git status"], shell=True,
                         capture_output=True, check=True)
    if "On branch master" in str(out):
        echo(
            f"You are on the master branch but we agreed to only use main... {angered_face}\n"
            f"Please rename the branch, darling {face_blowing_kiss}"
        )
        sys.exit()

    elif "On branch main" in str(out):
        echo(f"{face_screaming_in_fear} Cap, you are on main {face_screaming_in_fear}")
        ask_to_proceed()

    else:
        echo(
            "It seems like you are on a good branch.\n"
            f"The way is free for you to go ahead {magic_wand} {kissing_cat}"
        )


if __name__ == "__main__":
    verify_branch()
