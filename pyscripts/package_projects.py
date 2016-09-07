import os
import azure
import util
import pre_script
from runtime_tests import check_pkproj

def create_confirm_file():
    with io.open(util.savefile(".confirm_a"), 'w') as context:
        context.write("true")


def build_vms():
    if util.test_path(util.savefile(".confirm_a")):
        print("Service App already packaged")
    else:
        for vm_path in util.listdirpaths(util.SAVE_DIR):
            vm_name = vm_path.split("\\")[-1]
            check_pkproj.test_guid(vm_name)
            util.run_powershell("zip.ps1", {"ZipFileName": util.join_path(vm_path, util.get_zip_guid(vm_name)), "sourcedir": vm_path})
        create_confirm_file()
    check_pkproj.check_confirm_file()
    check_pkproj.check_zip_exists(util.join_path(vm_path, util.get_zip_guid(vm_name)))


def main(params):
    if params['mode'] == 'vm':
        print("Running in VM mode")
        build_vms()
    elif params['mode'] == 'vmss':
        print("Running in VMss mode")
    elif params['mode'] == 'pre':
        print("Running pre script")
        




if __name__ == "__main__":
    PARAMS = util.parse_input(DEFAULTS)
    assert PARAMS['mode'] in ['vmss', 'vm', 'pre'], "Invalid Mode!"
    main(PARAMS)
