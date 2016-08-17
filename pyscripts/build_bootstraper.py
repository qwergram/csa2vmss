# This script builds a bootstrapper for the worker role
import io
import json
import os
import shutil

def reset_sln(sln_location, to_remove):
    with io.open(sln_location) as context:
        sln_data = context.readlines()
    clean = []
    for line in sln_data:
        for guid in to_remove:
            if guid in line:
                break
        else:
            clean.append(line)

    clean_sln = "".join(clean).replace("EndProject\nEndProject\n", "EndProject\n")
    with io.open(sln_location, 'w') as context:
        context.write(clean_sln)

def run_powershell(name, arguments):
    arguments = " ".join(["-%s \"%s\"" % (key, value) for key, value in arguments.items()])
    execute_this = "powershell -ExecutionPolicy Unrestricted -File \"%s\" %s" % (os.path.join(CURRENT_PATH, 'psscripts', name), arguments)
    os.system(execute_this)

def copy_compiled_code(directory):
    bin_dest = os.path.join(directory, 'bin', '')

    def xcopy(project):
        bin_path_debug = os.path.join(directory, project, 'bin', 'Debug')
        bin_path_release = os.path.join(directory, project, 'bin', 'Release')
        if os.path.isdir(bin_path_release):
            origin_bin_path = bin_path_release
        elif os.path.isdir(bin_path_debug):
            origin_bin_path = bin_path_debug
        else:
            return
        os.system('xcopy \"%s\" \"%s\" /E /Y' % (origin_bin_path, bin_dest))

    for project in os.listdir(directory):
        if "bootstrap" not in project.lower():
            xcopy(project)

    for project in os.listdir(directory):
        if "bootstrap" in project.lower():
            xcopy(project)

    return bin_dest

def copy_schtask(location):
    shutil.copy(os.path.join(CURRENT_PATH, "templates", "schedule.xml"), os.path.join(location, "scheduler.xml"))

def zip_compiled_code(bin_location, zipfile):
    run_powershell('save_roles.ps1', {"zipfilename": zipfile, "sourcedir": bin_location})


def main(worker, solution, current_path, zip_package_name):
    # print(json.dumps(worker, indent=2))
    global CURRENT_PATH
    CURRENT_PATH = current_path
    solution['parent']['name'] = solution['parent']['folder'].split("\\")[-1]
    projects = [worker] + [project for project in solution['projects'] if not project.get('role_type')]
    to_remove = [project['guid'] for project in solution['projects'] if project not in projects] + [solution['parent']['guid']]
    project_dest = os.path.join(current_path, '__save', worker['guid'], "projects")

    for project in projects[::-1]:
        shutil.copytree(project['folder'], os.path.join(project_dest, project['name']))

    packaged_worker_sln = os.path.join(project_dest, solution['sln'].split("\\")[-1])
    shutil.copy(solution['sln'], packaged_worker_sln)
    reset_sln(packaged_worker_sln, to_remove)
    os.system("C:\\Windows\\Microsoft.NET\\Framework64\\v4.0.30319\\MSBuild.exe \"%s\"" % packaged_worker_sln)
    
    bin_location = copy_compiled_code(project_dest)
    copy_schtask(bin_location)
    zip_compiled_code(bin_location + "\\" if bin_location.endswith("\\") else bin_location, os.path.join(current_path, '__save', worker['guid'], "zip_" + worker['guid'][:4] + "_package.zip"))

    return solution
