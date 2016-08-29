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


def save_solution_data(project_name, solution_object):
    project_guid = name_to_guid(project_name, solution_object.solution_data)
    debug("Building save.json for", project_name)
    try:
        os.mkdir(os.path.join(CURRENT_PATH, '__save', project_guid))
    except FileExistsError:
        pass
    
    with io.open(os.path.join(CURRENT_PATH, '__save', project_guid, "save.json"), 'w') as context:
        context.write(json.dumps(solution_object.solution_data, indent=2, sort_keys=True))

    project = None
    for project in solution_object.solution_data['projects']:
        if project['name'] == project_name:
            break
    
    if project is None:
        raise FileNotFoundError("Project", project_name, project_guid, "Not Found")

    with io.open(os.path.join(CURRENT_PATH, '__save', project_guid, "meta.json"), 'w') as context:
        context.write(json.dumps(project, indent=2, sort_keys=True))


def name_to_guid(project_name, solution, silent_fail=False):
    for project in solution['projects']:
        if project['name'] == project_name == project_name:
            return project['guid']
    if silent_fail: return None
    raise FileNotFoundError(project_name, "not found")


def name_to_role(project_name, solution, silent_fail=False):
    for project in solution['projects']:
        if project['name'] == project_name:
            return project['role_type']
    if silent_fail: return None
    raise FileNotFoundError(project_name, "not found")


def get_zip_guid(project_guid):
    return "zip_" + project_guid[:4] + "_package.zip"


def requires_compilation(project_name, solution):
    for project in solution['projects']:
        if project['name'] == project_name:
            return project['compliation']


def package_solution(project_name, solution, keep=True):
    debug("Building", project_name)
    project_guid = name_to_guid(project_name, solution.solution_data)
    source_dir = os.path.join(CURRENT_PATH, '__save', 'vms', project_name)
    dest_dir = os.path.join(CURRENT_PATH, '__save', project_guid)
    zip_path = os.path.join(dest_dir, get_zip_guid(project_guid))
    prelim_path = os.path.join(dest_dir, 'pkg')

    os.mkdir(prelim_path)
    if name_to_role(project_name, solution.solution_data) == 'workerrole':
        debug("Copying workerrole binaries")
        for project in os.listdir(source_dir):
            if project.lower() == "bootstrap":
                debug_bin = os.path.join(source_dir, project, 'bin', 'Debug')
                release_bin = os.path.join(source_dir, project, 'bin', 'Release')
                source = os.path.join(source_dir, project)
                if os.path.isdir(release_bin):
                    bin_location = release_bin
                elif os.path.isdir(debug_bin):
                    bin_location = debug_bin
                elif requires_compilation(project_name, solution):
                    debug("Unable to find Bootstraper binaries for workerrole")
                    debug("Did you run `prescript.cmd -check`?")
                    sys.exit(1)
                else:
                    debug("Binaries not found. Using source code")
                    bin_location = source
                debug("Copying Bootstrapper")
                os.popen("xcopy \"{}\" \"{}\" /E".format(bin_location, prelim_path))
                break
        else:
            debug("Unable to locate Bootstrapper code")
            debug("Did you name the bootstrapper project `Bootstrap`?")
            sys.exit(1)
        debug("Copying scheduler for workerrole")
        sch_xml = os.path.join(CURRENT_PATH, 'templates', 'schedule.xml')
        shutil.copy(sch_xml, os.path.join(prelim_path, ''))
    else:
        for project in os.listdir(source_dir):
            project_path = os.path.join(source_dir, project)
            if os.path.isdir(project_path) and project != 'packages' and not project.startswith('.'):
                debug("Copying  %s.%s" % (project_name, project))
                try:
                    shutil.copytree(project_path, os.path.join(prelim_path, project))
                except shutil.Error:  # Weird bug with shutil.copy on windows when the absolute filepath is too long
                    os.popen("xcopy \"{}\" \"{}\" /E".format(project_path, os.path.join(prelim_path, project)))
            else:
                debug("Ignoring %s.%s" % (project_name, project))

    run_powershell("zip.ps1", {"zipfilename": zip_path, "sourcedir": prelim_path})
    if not keep:
        debug("Cleaning up mess")
        shutil.rmtree(prelim_path)


def clean():
    try:
        for directory in os.listdir(os.path.join(CURRENT_PATH, '__save')):
            path = os.path.join(CURRENT_PATH, '__save', directory)
            if (directory != "vms") and (".confirm" not in directory) and (".csv" not in directory):
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
    except FileNotFoundError:
        pass
    except OSError:
        debug("Can't delete the directory!'")
        debug("Is it open in another program?")
        sys.exit(1)


def write_confirm():
    with io.open(os.path.join(CURRENT_PATH, '__save', '.confirm_a'), 'w') as context:
        context.write("true")

def clean_roots(vm_path):
    debug("Cleansing", vm_path)
    for item in os.listdir(vm_path):
        item_path = os.path.join(vm_path, item)
        if os.path.isdir(item_path):
            for subdir in os.listdir(item_path):
                subdir_path = os.path.join(item_path, subdir)
                if subdir.lower() in ('env', 'obj', 'csx', 'ecf'):
                    try:
                        shutil.rmtree(subdir_path)
                    except OSError:
                        os.popen("rmdir /S /Q \"{}\"".format(subdir_path))

def main():
    clean()
    VM_PATH = os.path.join(CURRENT_PATH, "__save", "vms")
    if not os.path.isdir(VM_PATH):
        debug("VMs not found!")
        debug("Did you run the prescripts?")
        sys.exit(1)
    for vm_name in os.listdir(VM_PATH):
        vm_path = os.path.join(VM_PATH, vm_name)
        if os.path.isfile(vm_path): continue
        clean_roots(vm_path)
        solution = csa_parse.VSCloudService(project_path=vm_path)
        solution.load_solution()
        save_solution_data(vm_name, solution)
        package_solution(vm_name, solution)
    write_confirm()

if __name__ == "__main__":
    main()