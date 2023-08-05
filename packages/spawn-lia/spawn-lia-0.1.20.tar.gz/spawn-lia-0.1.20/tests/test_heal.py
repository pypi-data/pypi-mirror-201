import os
import shutil
from amarium.utils import copy_dir
from amarium.checks import check_delete_dir
import subprocess

from amarium.utils import search_subdirs


def test_heal_func():

    test_run_dir =  "tests/run"
    if os.path.isdir(test_run_dir):
        shutil.rmtree(test_run_dir)
    os.mkdir(test_run_dir)
    copy_dir("tests/package", test_run_dir)
    subprocess.run(["bash", "install.sh"])
    out = subprocess.run(["lia", "heal", "-t n" , test_run_dir], capture_output=True)
    assert "ModuleNotFoundError: No module named 'lia'" not in str(out)
    assert "No such option:" not in str(out)
    assert "error" not in str(out) or "Error" not in str(out)
