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


def read_vmss_params():
    with io.open(os.path.join(CURRENT_PATH, "templates", "iis-vm.params.json")) as context:
        return json.loads(context.read())


def set_vmss_params(vmss_params):
    params = parse_params()
    vmss_params['parameters'] = {}
    for param, value in params.items():
        if value.isdigit():
            value = int(value)
        elif value == "true":
            value = True
        elif value == "false":
            value = False
        elif value.replace('.', '').isdigit():
            value = float(value)
        elif value.startswith("{") and value.endswith("}"):
            value = json.loads(value)
            
        vmss_params['parameters'][param] = {"value": value}


def save_new_vmss_params(vmss_params):
    with io.open(os.path.join(CURRENT_PATH, "__save", "vmss_template_patched.params.json"), 'w') as context:
        context.write(json.dumps(vmss_params, indent=2, sort_keys=True))


def get_storage_profile(vm_json):
    storage_profile = vm_json["resources"][0]["properties"]["storageProfile"]
    try:
        del storage_profile['dataDisks']
    except KeyError:
        pass # It's already been deleted
    return storage_profile


def replace_storage_profile(vmss_json, storage_profile):
    for i, resource in enumerate(vmss_json["resources"]):
        if resource['type'] == "Microsoft.Compute/virtualMachineScaleSets":
            vmss_json['resources'][i]['properties']['virtualMachineProfile']['storageProfile'] = storage_profile
            return vmss_json


def parse_params():
    params = {}
    for item in sys.argv[1:]:
        if item.startswith('-') and "=" in item:
            key, value = item[1:].split('=', 1)
            params[key] = value
    return params


def save_new_vmss(json_blob):
    with io.open(os.path.join(CURRENT_PATH, "__save", "vmss_template_patched.json"), 'w') as context:
        context.write(json.dumps(json_blob, indent=2, sort_keys=True))


def main():
    imaged_vm = read_current_vm_template()
    vmss_to_deploy = read_vmss_template()
    vmss_params = read_vmss_params()
    set_vmss_params(vmss_params)
    save_new_vmss_params(vmss_params)
    storage_profile = get_storage_profile(imaged_vm)
    replace_storage_profile(vmss_to_deploy, storage_profile)
    save_new_vmss(vmss_to_deploy)


if __name__ == "__main__":
    PARAMS = parse_params()
    main()