import azure

import csa_parse
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


def destroy_binaries(vm_path):
    for file in ['env', 'obj', 'csx', 'ecf']:
        util.rmtree(os.path.join(vm_path, file))


def get_solution(vm_path):
    solution = csa_parse.VSCloudService(project_path=vm_path)
    solution.load_solution()
    return solution


def save_solution(vm_path, solution_object):
    pass

def build_vm():
    if util.test_path(util.savefile(".confirm_a")):
        print("Service App already packaged")
    else:
        util.clean()
        for vm_name, vm_path in util.list_vms():
            destroy_binaries(vm_path)
            solution = get_solution(vm_path)
            save_solution(vm_)

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
