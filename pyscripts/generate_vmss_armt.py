import sys
import os
import io
import json

CURRENT_PATH = os.getcwd()

PARAMETERS = {
    "vmSSName": {
        "value": "changeme"
    },
    "instanceCount": {
        "value": 2
    },
    "vmSize": {
        "value": "Standard_D1"
    },
    "dnsNamePrefix": {
        "value": "changeme"
    },
    "adminUsername": {
        "value": "changeme"
    },
    "adminPassword": {
        "value": "changeme"
    },
    "sourceImageVhdUri": {
        "value": "changeme"
    },
    "frontEndLBPort": {
        "value": 80
    },
    "backEndLBPort": {
        "value": 80
    }
}

PARAM_TEMPLATE = {}

def load_solution_data():
    with io.open(os.path.join(CURRENT_PATH, "__save", "screenshot.json")) as context:
        return json.loads(context.read())


def load_arm_params():
    with io.open(os.path.join(CURRENT_PATH, 'templates', 'iis-vm.params.json')) as content:
        template = json.loads(content.read())

    PARAMETERS['adminUsername']['value'] = SOLUTION_DATA['vmparams']['username']
    PARAMETERS['adminPassword']['value'] = SOLUTION_DATA['vmparams']['password']
    PARAMETERS['dnsNamePrefix']['value'] = SOLUTION_DATA['vmparams']['dnslabel']


if __name__ == "__main__":
    NAME = sys.argv[1]
    URI = sys.argv[2]
    SOLUTION_DATA = load_solution_data()
    print(json.dumps(SOLUTION_DATA['vmparams'], indent=2, sort_keys=True))
