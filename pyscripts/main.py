import json
import os
import io
import csa_parse
from csa_parse import debug
import shutil
import sys

CURRENT_PATH = os.getcwd()

def run_powershell(name, arguments):
    arguments = " ".join(["-%s \"%s\"" % (key, value) for key, value in arguments.items()])
    execute_this = "powershell -ExecutionPolicy Unrestricted -File \"%s\" %s" % (os.path.join(CURRENT_PATH, 'psscripts', name), arguments)
    os.system(execute_this)


def save_solution_data(project_guid, data):
    debug("Building save.json for", project_guid)
    try:
        os.mkdir(os.path.join(CURRENT_PATH, '__save', project_guid))
    except FileExistsError:
        pass
    
    with io.open(os.path.join(CURRENT_PATH, '__save', project_guid, "save.json"), 'w') as context:
        context.write(json.dumps(data.solution_data, indent=2, sort_keys=True))


def name_to_guid(project_name, solution, silent_fail=False):
    for project in solution['projects']:
        if project['name'] == project_name:
            return project['guid']
    else:
        if silent_fail: return None
        raise FileNotFoundError(project_name, "not found")


def get_zip_guid(project_guid):
    return "zip_" + project_guid[:4] + "_package.zip"


def package_solution(project_name, solution, keep=True):
    debug("Building", project_name)
    project_guid = name_to_guid(project_name, solution.solution_data)
    source_dir = os.path.join(CURRENT_PATH, '__save', 'vms', project_name)
    dest_dir = os.path.join(CURRENT_PATH, '__save', project_guid)
    zip_path = os.path.join(dest_dir, get_zip_guid(project_guid))
    prelim_path = os.path.join(dest_dir, 'pkg')
    for project in os.listdir(source_dir):
        
        project_path = os.path.join(source_dir, project)
        if os.path.isdir(project_path) and project != 'packages' and not project.startswith('.'):
            debug("Copying  %s.%s" % (project_name, project))
            try:
                shutil.copytree(project_path, os.path.join(prelim_path, project))
            except shutil.Error:
                os.popen("xcopy \"{}\" \"{}\" /E".format(project_path, os.path.join(prelim_path, project)))
        else:
            debug("Ignoring %s.%s" % (project_name, project))
    
    run_powershell("zip.ps1", {"zipfilename": zip_path, "sourcedir": prelim_path})
    if not keep:
        shutil.rmtree(prelim_path)


def clean():
    try:
        for directory in os.listdir(os.path.join(CURRENT_PATH, '__save')):
            path = os.path.join(CURRENT_PATH, '__save', directory)
            if directory != "vms":
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
    except FileNotFoundError:
        pass


def write_confirm():
    with io.open(os.path.join(CURRENT_PATH, '__save', '.confirm_a'), 'w') as context:
        context.write()


def main():
    clean()
    VM_PATH = os.path.join(CURRENT_PATH, "__save", "vms")
    for vm_name in os.listdir(VM_PATH):
        vm_path = os.path.join(VM_PATH, vm_name)
        if os.path.isfile(vm_path): continue
        solution = csa_parse.VSCloudService(project_path=vm_path)
        solution.load_solution()
        save_solution_data(name_to_guid(vm_name, solution.solution_data), solution)
        package_solution(vm_name, solution)
    write_confirm()

if __name__ == "__main__":
    main()