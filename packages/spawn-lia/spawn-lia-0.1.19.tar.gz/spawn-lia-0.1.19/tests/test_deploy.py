import os
import shutil
from amarium.utils import copy_dir
from amarium.checks import check_delete_dir
import subprocess

from amarium.utils import search_subdirs


def test_deploy_func(): 

    build_dir = "./build"
    dist_dir = "./dist"
    check_delete_dir(build_dir)
    check_delete_dir(dist_dir)
    # two times installation is not neccessary
    out = subprocess.run(["lia", "deploy", "-t n"], capture_output=True)
    assert "ModuleNotFoundError: No module named 'lia'" not in str(out)
    assert "No such option:" not in str(out)
    assert "Successfully built" in str(out)
    assert os.path.isdir(dist_dir) == True