import os
import azure
import util
import pre_script

def destroy_binaries(vm_path):
    for file in ['env', 'obj', 'csx', 'ecf']:
        util.rmtree(os.path.join(vm_path, file), silent=True)


def get_solution(vm_path):
    solution = csa_parse.VSCloudService(project_path=vm_path)
    solution.load_solution()
    return solution


def create_guid_directory():
    pass


def save_solution(vm_path, solution_object):
    util.save_json(solution_object.solution_data)


def build_vm():
    if util.test_path(util.savefile(".confirm_a")):
        print("Service App already packaged")
    else:
        util.clean()
        for vm_name, vm_path in util.list_vms():
            destroy_binaries(vm_path)
            solution = get_solution(vm_path)
            input(solution)
            # save_solution(vm_path, solution)

def main(params):
    if params['mode'] == 'vm':
        print("Running in VM mode")
    elif params['mode'] == 'vmss':
        print("Running in VMss mode")
    elif params['mode'] == 'pre':
        print("Running pre script")
        




if __name__ == "__main__":
    PARAMS = util.parse_input(DEFAULTS)
    assert PARAMS['mode'] in ['vmss', 'vm', 'pre'], "Invalid Mode!"
    main(PARAMS)