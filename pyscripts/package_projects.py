import os
import azure
import util
import pre_script

def destroy_binaries(vm_path):
    for file in ['env', 'obj', 'csx', 'ecf']:
        util.rmtree(os.path.join(vm_path, file), silent=True)


def build_vms():
    if util.test_path(util.savefile(".confirm_a")):
        print("Service App already packaged")
    else:
        for vm_path in util.listdirpaths(util.SAVE_DIR):
            vm_name = vm_path.split("\\")[-1]
            destroy_binaries(vm_path)

def main(params):
    if params['mode'] == 'vm':
        build_vms()
        print("Running in VM mode")
    elif params['mode'] == 'vmss':
        print("Running in VMss mode")
    elif params['mode'] == 'pre':
        print("Running pre script")
        




if __name__ == "__main__":
    PARAMS = util.parse_input(DEFAULTS)
    assert PARAMS['mode'] in ['vmss', 'vm', 'pre'], "Invalid Mode!"
    main(PARAMS)
