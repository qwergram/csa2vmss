import sys
import os
import io
import json
import shutil

CURRENT_PATH = os.getcwd()

def read_current_vm_template():
    with io.open(os.path.join(CURRENT_PATH, "__save", "vmss_template.json")) as context:
        return json.loads(context.read())

def read_vmss_template():
    with io.open(os.path.join(CURRENT_PATH, "templates", "vmss.json")) as context:
        return json.loads(context.read())


def main():
    pass

if __name__ == "__main__":
    main()