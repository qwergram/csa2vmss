import io
import util
import pre_script
from runtime_tests import check_pkproj

def create_confirm_file():
    with io.open(util.savefile(".confirm_a"), 'w') as context:
        context.write("true")


def clean_package(vm_name):
    check_pkproj.test_guid(vm_name)
    solution = pre_script.get_solution_data(util.join_path(util.SAVE_DIR, vm_name, "{0}.sln".format(vm_name)), False)
    solution.parse()
    solution.data['csdef'] = "somestring"
    solution.data['ccproj'] = "somestring"
    solution.data['cscfg'] = "somestring"
    check_pkproj.test_solution(solution)
    for project in solution.data['projects']:
        location = project['location']
        lang = project['type']
        ignores = util.get_ignores(lang)
        for path in util.listdirpaths(location):
            for ignore in ignores:
                if ignore in path:
                    print(path)
                    util.rmtree(path)


def build_vms():
    if util.test_path(util.savefile(".confirm_a")):
        print("Service App already packaged")
    else:
        for vm_path in util.listdirpaths(util.SAVE_DIR):
            vm_name = vm_path.split("\\")[-1]
            check_pkproj.test_guid(vm_name)
            clean_package(vm_name)
            # util.run_powershell("zip.ps1", {"ZipFileName": util.join_path(vm_path, util.get_zip_guid(vm_name)), "SourceDir": vm_path})
            check_pkproj.check_zip_exists(util.join_path(vm_path, util.get_zip_guid(vm_name)))
        create_confirm_file()
    check_pkproj.check_confirm_file()


def main(params):
    if params['mode'] == 'vm':
        print("Running in VM mode")
        build_vms()
    elif params['mode'] == 'vmss':
        print("Running in VMss mode")
    elif params['mode'] == 'pre':
        print("Running pre script")


if __name__ == "__main__":
    PARAMS = util.parse_input({"mode": "vm"})
    assert PARAMS['mode'] in ['vmss', 'vm', 'pre'], "Invalid Mode!"
    main(PARAMS)
