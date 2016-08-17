import sys
import os
import io
import json

CURRENT_PATH = os.getcwd()

PARAMETERS = {
    "vmSSName": {
        "value": None
    },
    "instanceCount": {
        "value": 2
    },
    "vmSize": {
        "value": "Standard_D1"
    },
    "dnsNamePrefix": {
        "value": None
    },
    "adminUsername": {
        "value": None
    },
    "adminPassword": {
        "value": None
    },
    "sourceImageVhdUri": {
        "value": None
    },
    "frontEndLBPort": {
        "value": 80
    },
    "backEndLBPort": {
        "value": 80
    }
}

with io.open(os.path.join(CURRENT_PATH, "templates", "vmss.json")) as vmss_context:
    VMSS_ARMT = json.loads(vmss_context.read())

with io.open(os.path.join(CURRENT_PATH, "templates", "vmss.params.json")) as vmss_param_context:
    VMSS_PARAMS_ARMT = json.loads(vmss_param_context.read())

def load_solution_data():
    with io.open(os.path.join(CURRENT_PATH, "__save", "screenshot.json")) as context:
        return json.loads(context.read())

def load_arm_params():
    with io.open(os.path.join(CURRENT_PATH, 'templates', 'iis-vm.params.json')) as content:
        template = json.loads(content.read())

    PARAMETERS['adminUsername']['value'] = SOLUTION_DATA['vmparams']['username']
    PARAMETERS['adminPassword']['value'] = SOLUTION_DATA['vmparams']['password']
    PARAMETERS['dnsNamePrefix']['value'] = NAME[0] + SOLUTION_DATA['vmparams']['dnslabel']
    PARAMETERS['sourceImageVhdUri']['value'] = URI
    PARAMETERS["vmSSName"]['value'] = NAME.lower().replace("vm", 'vmss')

def save_arm_params():
    location = os.path.join(CURRENT_PATH, "__save", "vmss_" + NAME, "")
    try:
        os.mkdir(location)
    except FileExistsError:
        pass
    with io.open(os.path.join(location, "vmss.params.json"), 'w') as context:
        context.write(json.dumps(VMSS_PARAMS_ARMT, indent=2, sort_keys=True))

if __name__ == "__main__":
    NAME = sys.argv[1]
    URI = sys.argv[2]
    SOLUTION_DATA = load_solution_data()
    load_arm_params()
    VMSS_PARAMS_ARMT["parameters"] = PARAMETERS
    save_arm_params()

    print(json.dumps(VMSS_PARAMS_ARMT, indent=2, sort_keys=True))