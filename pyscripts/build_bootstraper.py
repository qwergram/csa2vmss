# This script builds a bootstrapper for the worker role
import io
import json
import os
import shutil

def load_appconfig(location):
    print("Load app.config")
    with io.open(location) as context:
        return context.read()

def load_assemblyinfo(location):
    with io.open(location) as context:
        return context.read()

def load_csproj(location):
    with io.open(location) as context:
        return context.read()


def load_bootstrapper(location, workername, classname):
    with io.open(location) as context:
        bootstrap = context.read()
    bootstrap = bootstrap.replace("{$WORKERNAME!}", workername).replace("{$CLASSNAME!}", classname)
    return bootstrap

def main(worker, solution, current_path):
    # print(json.dumps(worker, indent=2))
    projects = [worker] + [project for project in solution['projects'] if not project.get('role_type')]
    to_remove = [project['name'] for project in solution['projects'] if project not in projects]
    input(to_remove)
    project_dest = os.path.join(current_path, '__save', worker['guid'], "projects")

    for project in projects[::-1]:

        project_binaries_release = os.path.join(project['folder'], 'bin', 'Release', '')
        project_binaries_debug = os.path.join(project['folder'], 'bin', 'Debug', '')

        if os.path.isdir(project_binaries_release):
            project_binaries = project_binaries_release
            for i, _project in enumerate(solution['projects']):
                if _project == project:
                    solution['projects'][i].setdefault('bins', {})['release'] = project_binaries_release

        elif os.path.isdir(project_binaries_debug):
            project_binaries = project_binaries_debug
            for i, _project in enumerate(solution['projects']):
                if _project == project:
                    solution['projects'][i].setdefault('bins', {})['debug'] = project_binaries_debug
        else:
            raise FileNotFoundError("project binaries not found. Please build package before proceeding!")

        shutil.copytree(project['folder'], os.path.join(project_dest, project['name']))

    shutil.copy(solution['sln'], project_dest)

    # global APPCONFIG, ASSEMBLIES, CSPROJ, BOOTSTRAP
    # print("Building bootstrapper")
    # APPCONFIG = load_appconfig()
    # ASSEMBLIES = load_assemblyinfo()
    # CSPROJ = load_csproj()
    # BOOTSTRAP = load_bootstrapper()

    return solution

if __name__ == "__main__":
    main()
