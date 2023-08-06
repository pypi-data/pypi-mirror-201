"""This is lia's main program.

:author: Julian M. Kleber
"""
import os
import subprocess

import click
from click import echo

from lia.check_git.verify_branch import verify_branch
from lia.conversation.end_message import say_end_message
from lia.conversation.start_message import say_start_message

# spells
from lia.simplify.create_venv import create_venv


@click.group()
def spells() -> None:
    """Collection for Lia's spells.

    For more info ask for help on each specific spell.
    """
    pass  # pragma: no cover


@click.command()
@click.argument("packagename")
@click.option("-t", default="y", help="If test should be run")
def heal(packagename: str, t: str) -> None:  # pragma: no cover
    """One of Lias most basic spells. It lints, and typechecks the code
    specified in the path. To test use the -t option. Lia only supports pytest.

    The heal function is a wrapper for the following commands:
        - black
        - autopep8
        - flake8 (with E9, F63, F7 and F82)
        - mypy --strict
       It also runs pylint with the parseable output format to
       make it easier to integrate into CI systems like
       Woodpecker or Codeberg CI.

    :param packagename:str: Used to specify the package name.
    :param o:str: Used to specify if the user wants to run tests or not.

    :doc-author: Julian M. Kleber
    """
    say_start_message()
    verify_branch()
    assert t in ["y", "n"], "Plase specify -t as y/n"
    assert os.path.isdir(packagename)
    if not packagename.endswith("/"):
        packagename += "/"
    subprocess.run(["pip freeze > requirements.txt"], shell=True, check=True)
    subprocess.run(["black " + packagename], shell=True, check=True)
    subprocess.run(
        [
            f"find . -type f -wholename '{packagename}/*.py' "
            "-exec sed --in-place 's/[[:space:]]\+$//' "
            + "{} \+ #sanitize trailing whitespace"
        ],
        shell=True,
        check=True,
    )
    subprocess.run(
        [f"autopep8 --in-place --recursive {packagename}"], shell=True, check=True
    )
    subprocess.run(
        [
            f"python -m flake8 {packagename} --count --select=E9,F63,F7,F82"
            " --show-source --statistics"
        ],
        shell=True,
        check=True,
    )
    try:
        subprocess.run(
            [f"mypy --strict {packagename}"], shell=True, check=True)
    except Exception as exc:
        print(str(exc))

    try:
        subprocess.run(
            [f"python -m pylint -f parseable {packagename}"], shell=True, check=True
        )
    except Exception as exc:
        print(str(exc))
    subprocess.run(
        [f"prettify-py format-dir {packagename}"], shell=True, check=True)
    if t == "y":
        try:
            subprocess.run(["python -m pytest tests/"], shell=True, check=True)
        except Exception as exc:
            print(str(exc))
    say_end_message()


@click.command()
@click.option("-t", default="y", help="If test should be run")
def deploy(t: str) -> None:
    """Deployment routine.

    :author: Julian M. Kleber
    """
    say_start_message()
    verify_branch()
    if t == "y":
        out = subprocess.run(
            ["python -m pytest tests/"], shell=True, check=True, capture_output=True
        )
        try:
            assert "FAILED" not in str(out)
        except:
            echo(out)
        finally:
            echo("Done testing.")
    if os.path.isdir("dist") is True:
        subprocess.run(["rm -r dist "], shell=True, check=True)
    if os.path.isdir("build") is True:
        subprocess.run(["rm -r build"], shell=True, check=True)
    subprocess.run(["python3 -m build"], shell=True, check=True)
    subprocess.run(["twine check dist/*"], shell=True, check=True)
    subprocess.run(["python3 -m twine upload dist/*"], shell=True, check=True)
    say_end_message()


spells.add_command(heal)
spells.add_command(deploy)
spells.add_command(create_venv)

if __name__ == "__main__":
    spells()
