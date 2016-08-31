import azure

import util

DEFAULTS = {
    "solutionName": "SP55",
    "resourcePrefix": "RG",
    "storagePrefix": "stg",
    "VMPrefix": "VM",
    "Location": "West US",
    "SkuName": "Standard_LRS",
    "containerPrefix": "container",
    "DNSPrefix": "dns",
    "DeploymentPrefix": "deploy",
    "scriptPrefix": "scrpt",
    "VMVHDSize": 100,
    "VMSize": "Standard_D1",
    "VMAdmin": "Norton",
    "VMPassword": "SecurePassword123!"
}


def build_vm():
    if util.test_path(util.savefile(".confirm_a")):
        print("Service App already packaged")


def main(params):
    if params['mode'] == 'vm':
        print("Running in VM mode")
        build_vm()
    elif params['mode'] == 'vmss':
        print("Running in VMss mode")
        




if __name__ == "__main__":
    PARAMS = util.parse_input(DEFAULTS)
    assert PARAMS['mode'] in ['vmss', 'vm'], "Invalid Mode!"
    main(PARAMS)
