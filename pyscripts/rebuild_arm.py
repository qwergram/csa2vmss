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


def get_storage_profile(vm_json):
    return vm_json["resources"][0]["properties"]["storageProfile"]


def parse_params():
    params = {}
    for item in sys.argv[1:]:
        if item.startswith('-') and "=" in item:
            key, value = item[1:].split('=', 1)
            params[key] = value
    return params


def main():
    imaged_vm = read_current_vm_template()
    vmss_to_deploy = read_vmss_template()




if __name__ == "__main__":
    PARAMS = parse_params()
    main()