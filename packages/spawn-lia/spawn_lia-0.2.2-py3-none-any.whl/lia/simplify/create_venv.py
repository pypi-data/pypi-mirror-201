"""
Helping with venv operations to avoid confusions

:author: Julian M. Kleber
"""

import subprocess
from amarium.utils import append_slash
import click
from click import echo

from lia.conversation.virtualenv import is_activated


@click.command()
@click.argument("directory")
def create_venv(directory: str) -> None:
    """
    The create_venv function creates a virtual environment in the directory
    specified by the user. It first checks to see if there is an active virtual
    environment, and if so, it asks the user whether they would like to deactivate
    it before creating a new one. If not, it creates a new venv called "venv" in
    the specified directory.

    :param directory: Used to Create a virtual environment in the.
    :return: None.

    :doc-author: Julian M. Kleber
    """

    venv_check = check_venv()
    venv_path = venv_check.decode("utf-8").replace("\n", "")
    if len(venv_check) > 0:
        message = is_activated(venv_path=venv_path)
        echo(message=message)
        echo(message="Please run:\n\ndeactivate")
        # shall_i_deactivate(venv_path=venv_path)  # ask to deactivate

    venv_name = append_slash(directory) + "venv"
    subprocess.run([f"python3 -m venv {venv_name}"], shell=True, check=True)
    subprocess.run([f"source {venv_name}/bin/activate"],
                   shell=True, check=True)


def check_venv() -> bytes:
    """
    The check_venv function checks to see if the user is in a virtual environment.
    If they are, it returns the path to that virtual environment. If not, it raises an error.

    :return: A byte string.

    :doc-author: Julian M. Kleber
    """

    out = subprocess.run(
        ["echo $VIRTUAL_ENV"], shell=True, check=True, capture_output=True
    )
    return out.stdout
