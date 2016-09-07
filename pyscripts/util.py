import io
import json
import os
import shutil
import sys
import mimetypes

SAVE_DIR = os.path.join(os.getcwd(), "__save")
PYSCRIPTS = os.path.join(os.getcwd(), "pyscripts")
PSSCRIPTS = os.path.join(os.getcwd(), "psscripts")
CMDSCRIPTS = os.path.join(os.getcwd(), "cmdscripts")
POST_TEST_ENV = os.path.join(os.getcwd(), 'tests', 'test_env', 'post')
PRE_TEST_ENV = os.path.join(os.getcwd(), 'test', 'test_env', 'pre')

DEBUG = True


class BatchTest(object):

    def __init__(self, test_functions, input_values, results, messages):
        assert isinstance(input_values, list)
        assert isinstance(test_functions, list)
        for i, test_function in enumerate(test_functions):
            self.test(test_function, input_values[i], results[i], messages[i])

    def test(self, test_function, args, result, message):
        assert test_function(*args) == result, message


def save_test_results(total):
    testresults = savefile(".testresults")
    results = total
    if test_path(testresults):
        with io.open(testresults) as context:
            try:
                results = int(context.read().strip())
            except ValueError:
                results = total
    with io.open(testresults, 'w') as context:
        context.write(testresults)
    return [total, results]


def debug(*args, **kwargs):
    if DEBUG:
        print("[!]", *args, **kwargs)


def load_xml(location):
    import xml.etree.ElementTree
    root = xml.etree.ElementTree.parse(location).getroot()
    return root


def parse_input_args(defaults=None):
    if defaults is None: defaults = []
    for item in sys.argv[1:]:
        if item.startswith('-') and '=' in item:
            continue
        defaults.append(item)
    return defaults


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


def pyscript(file, silent=True):
    path = os.path.join(PYSCRIPTS, file)
    assert test_path(path, "f") or silent
    return path


def psscript(file, silent=True):
    path = os.path.join(PSSCRIPTS, file)
    assert test_path(path, "f") or silent
    return path


def cmdscript(file, silent=True):
    path = os.path.join(CMDSCRIPTS, file)
    assert test_path(path, "f") or silent
    return path

def savefile(file, silent=True):
    path = os.path.join(SAVE_DIR, file)
    assert test_path(path, "a") or silent
    return path


def rmtree(path, silent=False):
    exists = test_path(path)
    if exists:
        try:
            shutil.rmtree(path)
        except OSError:
            os.popen("rmdir /S /Q \"{}\"".format(path))
    elif not silent:
        raise FileNotFoundError("{} not found".format(path))


def clean():
    for directory in listdirpaths(SAVE_DIR):
        rmtree(directory)

def save_json(python_object, path, filename=None):
    if filename: path = os.path.join(path, filename)
    with io.open(os.path.join(path), 'w') as context:
        context.write(json.dumps(python_object, indent=2, sort_keys=True))

def mkdir(path, dir_name=None, silent=True):
    try:
        if dir_name:
            os.mkdir(os.path.join(path, dir_name))
        else:
            os.mkdir(path)
    except FileExistsError as e:
        if not silent:
            raise FileExistsError(e)
    except PermissionError:
        raise PermissionError("Invalid Permissions. Try running ad admin?")


def copytree(source_dir, dest_dir, silent=False, override=True):
    source_exists = test_path(source_dir)
    dest_exists = test_path(dest_dir)
    if source_exists and (override or not dest_exists):
        try:
            shutil.copytree(source_dir, dest_dir)
        except shutil.Error:
            os.popen("xcopy \"{}\" \"{}\" /E".format(source_dir, dest_dir))
        except FileExistsError:
            rmtree(dest_dir)
            copytree(source_dir, dest_dir, silent, override)
    elif not silent and not source_exists:
        raise FileNotFoundError("{} does not exist".format(source_dir))
    elif not silent and dest_exists:
        raise FileExistsError("{} already exists".format(dest_dir))


def join_path(*args):
    to_return = []
    for arg in args:
        if arg.endswith(":"):
            arg += os.sep
        to_return.append(arg)
    return os.path.join(*to_return)


def listdirpaths(path):
    for file in os.listdir(path):
        yield join_path(path, file)


def load_solution_from_json(directory):
    assert test_path(directory, 'd')
    for file_path in listdirpaths(directory):
        if file_path.endswith("ctv.properties"):
            with io.open(file_path) as context:
                return json.loads(context.read())


def run_powershell(name, arguments):
    arguments = " ".join(["-%s \"%s\"" % (key, value) for key, value in arguments.items()])
    execute_this = "powershell -ExecutionPolicy Unrestricted -File \"%s\" %s" % (os.path.join(PSSCRIPTS, name), arguments)
    os.system(execute_this)


def walk_tree(path):
    for path in listdirpaths(path):
        if test_path(path, 'd'):
            yield from walk_tree(path)
        elif test_path(path, 'f'):
            yield path


def is_binary(path, silent=True):
    binaries = [
        'application/x-msdownload'
    ]
    extensions = [
        '.nupkg'
    ]
    if test_path(path, 'f') or silent:
        return (mimetypes.guess_type(path)[0] in binaries) or (path.split("\\")[-1] in extensions)
    else:
        raise FileNotFoundError(path, "not found")
