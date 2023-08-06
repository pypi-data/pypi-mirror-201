import subprocess
from subprocess import Popen, PIPE
from lia.conversation import ask_to_proceed
from lia.check_git import verify_branch


def test_verify_branch():
    # case 1

    out = subprocess.Popen(
        ["python", "./lia/conversation/ask_to_proceed.py"], stdin=PIPE, stdout=PIPE
    )
    out.stdin.write(b"y\n")
    outputlog, errorlog = out.communicate()
    out.stdin.close()

    assert errorlog is None
    assert (
        b"Are you sure that you want to proceed \xf0\x9f\x98\xa8? (y/n)\nGood decision, darling \xf0\x9f\xaa\x84 \xf0\x9f\x98\xbd\n"
        == outputlog
    )
    # case 2
    out = subprocess.Popen(
        ["python", "./lia/conversation/ask_to_proceed.py"], stdin=PIPE, stdout=PIPE
    )
    out.stdin.write(b"n\n")
    outputlog, errorlog = out.communicate()
    out.stdin.close()
    assert errorlog is None
    assert (
        b"Are you sure that you want to proceed \xf0\x9f\x98\xa8? (y/n)\nOkay, I guess you got this... \xf0\x9f\x98\x94\n"
        == outputlog
    )

    # case 3
    out = subprocess.Popen(
        ["python", "./lia/conversation/ask_to_proceed.py"], stdin=PIPE, stdout=PIPE
    )
    out.stdin.write(b"Don't know\n")
    outputlog, errorlog = out.communicate()
    out.stdin.close()
    assert errorlog is None
    assert (
        b"Are you sure that you want to proceed \xf0\x9f\x98\xa8? (y/n)\nYou have to decide y/n, darling...\xf0\x9f\x99\x84\n"
        == outputlog
    )


def test_continue_func():
    # safety add
    subprocess.run(["git add . "], check=True, shell=True)
    subprocess.run(["git", "commit", '-m"the work was automatically commited by test"'])
    # case 1 on a good branch
    try:
        subprocess.run(["git checkout -b dev"], check=True, shell=True)
    except:
        print("branch already exists")
    finally:
        subprocess.run(["git checkout dev"], check=True, shell=True)
    out = subprocess.Popen(
        ["python", "./lia/check_git/verify_branch.py"], stdin=PIPE, stdout=PIPE
    )
    # out.stdin.write(b"y\n")
    outputlog, errorlog = out.communicate()
    out.stdin.close()
    assert (
        outputlog
        == b"It seems like you are on a good branch.\nThe way is free for you to go ahead \xf0\x9f\xaa\x84 \xf0\x9f\x98\xbd\n"
    )
    assert errorlog is None

    # case 2 on master
    try:
        subprocess.run(["git checkout -b master"], check=True, shell=True)
    except:
        print("branch already exists")
    finally:
        subprocess.run(["git checkout master"], check=True, shell=True)
    out = subprocess.Popen(
        ["python", "./lia/check_git/verify_branch.py"], stdin=PIPE, stdout=PIPE
    )
    out.stdin.write(b"y\n")
    outputlog, errorlog = out.communicate()
    out.stdin.close()

    assert (
        outputlog
        == b"You are on the master branch but we agreed to only use main... \xf0\x9f\x98\xa1\nPlease rename the branch, darling \xf0\x9f\x98\x98\n"
    )
    assert errorlog is None

    subprocess.run(["git checkout dev"], shell=True, check=True)
    subprocess.run(["git branch -D master"], check=True, shell=True)

    # case 3 on main
    """try:
        subprocess.run(["git checkout -b main"], check=True, shell=True)
    except: 
        print("branch already exists")
    finally: 
        subprocess.run(["git checkout main"], check=True, shell=True)
    out = subprocess.Popen(
        ["python", "./lia/check_git/verify_branch.py"], stdin=PIPE, stdout=PIPE
    )
    out.stdin.write(b"y\n")
    outputlog, errorlog = out.communicate()
    out.stdin.close()

    assert 1 == 2, str(outputlog)
    assert outputlog == b"We don't use master branches any longer \xf0\x9f\x98\xa1\nPlease rename the branch, darling \xf0\x9f\x98\x98\n"
    assert errorlog is None

    subprocess.run(["git checkout dev"], shell=True, check=True)
   """  # -> can only implement after merge
