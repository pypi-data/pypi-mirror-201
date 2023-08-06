import os
import subprocess


def test_creating_venv_func():
    # prepare

    # no venv actiavated
    out = subprocess.run(
        ["lia create-venv tests/test_venv"], shell=True, check=True, capture_output=True
    )
    assert "venv" in os.listdir("tests/test_venv")
    # venv activated
    out = subprocess.run(
        ["lia create-venv tests/test_venv"], shell=True, check=True, capture_output=True
    )
    assert (
        b"\n\xf0\x9f\x92\x94\xf0\x9f\x92\x94\xf0\x9f\x92\x94\nOh, no! You have already a virtualenv activated \xf0\x9f\x99\x84\nI recommend to deactivate the running virtualenv \xf0\x9f\x98\xbd\xf0\x9f\xaa\x84\n\xf0\x9f\x91\x87The venv is in\xf0\x9f\x91\x87\n\n/home/developer/lia/venv\nPlease run:\n\ndeactivate\n"
        == out.stdout
    )
