import sys
import os
import shutil

SAVE_DIR = os.path.join(os.getcwd(), "__save")
PYSCRIPTS = os.path.join(os.getcwd(), "pyscripts")
PSSCRIPTS = os.path.join(os.getcwd(), "psscripts")
CMDSCRIPTS = os.path.join(os.getcwd(), "cmdscripts")
VMPATH = os.path.join(SAVE_DIR, "vms")

def parse_input(defaults=None):
    if defaults is None: defaults = {}
    for item in sys.argv[1:]:
        if item.startswith('-') and '=' in item:
            key, value = item[1:].split('=', 1)
            if value.isdigit(): value = int(value)
            elif value.replace('.', '').isdigit(): value = float(value)
            elif value.lower() == "true": value = True
            elif value.lower() == "false": value = False
            defaults[key] = value
    return defaults

def test_path(path, mode="any"):
    isdir = os.path.isdir(path)
    isfile = os.path.isfile(path)
    if mode[0] == "a":
        return isdir or isfile
    elif mode[0] == "f":
        return isfile
    elif mode[0] == "d":
        return isdir
    else:
        raise ValueError("Invalid mode {}".format(mode))


def pyscript(file):
    path = os.path.join(PYSCRIPTS, file)
    assert test_path(path, "f")
    return path


def psscript(file):
    path = os.path.join(PSSCRIPTS, file)
    assert test_path(path, "f")
    return path


def cmdscript(file):
    path = os.path.join(CMDSCRIPTS, file)
    assert test_path(path, "f")
    return path

def savefile(file):
    path = os.path.join(SAVE_DIR, file)
    assert test_path(path, "a")
    return path


def rmtree(path):
    try:
        shutil.rmtree(path)
    except OSError:
        os.popen("rmdir /S /Q \"{}\"".format(path))


def clean():
    for directory in os.listdir(SAVE_DIR):
        path = os.path.join(SAVE_DIR, directory)
        if (directory != "vms"):
            rmtree(path)