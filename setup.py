import os
import subprocess
from pathlib import Path

import cli
from setuptools import find_packages, setup

NAME = "tbhandler"


def read(filename):
    try:
        with open(filename) as fp:
            content = fp.read().split("\n")
    except FileNotFoundError:
        content = []
    return content


def remove_other_sitecustomize():
    finished = False
    while not finished:
        try:
            sitecustomize_file = cli.get(
                "python3 -c 'import sitecustomize; print(sitecustomize.__file__)'"
            )
        except ModuleNotFoundError:
            finished = True
        else:
            path = Path(sitecustomize_file)
            if not (path.parent / "setup.py").exists():
                try:
                    path.unlink()
                except PermissionError:
                    if os.name == "posix":
                        args = ["sudo", "rm", path]
                        if "SUDO_ASKPASS" in os.environ:
                            args.insert(1, "-A")
                        subprocess.run(args)
                    else:
                        finished = True
                except FileNotFoundError:
                    finished = True
            else:
                finished = True


remove_other_sitecustomize()

setup(
    author="Quinten Roets",
    author_email="quinten.roets@gmail.com",
    description="gui",
    name=NAME,
    version="1.0",
    packages=find_packages(),
    py_modules=["sitecustomize"],
    install_requires=read("requirements.txt"),
)
