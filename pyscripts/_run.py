import sys
import os
import io
import json
import pyscripts.csa_parse
import pyscripts.build_bootstraper
import shutil

CURRENT_PATH = os.getcwd()
LAZY = True


def parse(enum, content):
    if content.startswith("-") and '=' in content:
        return (content.split('=')[0][1:], content.split('=')[1])
    else:
        return enum, content


def load_solution(location):
    parsed = pyscripts.csa_parse.VSCloudService(location)
    parsed.load_solution()
    solution = parsed.solution_data
    solution['origin'] = location
    solution['sln'] = os.path.join(location, [f for f in os.listdir(location) if f.lower().endswith('.sln')][0])
    print(json.dumps(solution, indent=2, sort_keys=True))
    return solution


def run_powershell(name, arguments):
    arguments = " ".join(["-%s \"%s\"" % (key, value) for key, value in arguments.items()])
    execute_this = "powershell -ExecutionPolicy Unrestricted -File \"%s\" %s" % (os.path.join(CURRENT_PATH, 'psscripts', name), arguments)
    os.system(execute_this)


def package_projects(solution):
    for project in solution['projects']:
        project.setdefault("instances", 1)
        project.setdefault("role_type", None)
        if project['role_type'] == 'webrole':
            os.mkdir(os.path.join(CURRENT_PATH, '__save', project['guid']))
            with io.open(os.path.join(CURRENT_PATH, '__save', project['guid'], "meta.json"), 'w') as f:
                f.write(json.dumps(project, indent=2))
                run_powershell("save_roles.ps1", {"zipfilename": os.path.join(CURRENT_PATH, '__save', project['guid'], "zip_" + project['guid'][:4] + "_package.zip"), "sourcedir": project['folder'] + "\\" if project['folder'].endswith("\\") else project['folder']})
        elif project['role_type'] == 'workerrole':
            os.mkdir(os.path.join(CURRENT_PATH, '__save', project['guid']))
            with io.open(os.path.join(CURRENT_PATH, '__save', project['guid'], "meta.json"), 'w') as f:
                f.write(json.dumps(project, indent=2))
                solution = pyscripts.build_bootstraper.main(project, solution, CURRENT_PATH, os.path.join(CURRENT_PATH, '__save', project['guid'], "zip_" + project['guid'][:4] + "_package.zip"))

def clean():
    try:
        for directory in os.listdir(os.path.join(CURRENT_PATH, '__save')):
            path = os.path.join(CURRENT_PATH, '__save', directory)
            if directory != "vms":
                shutil.rmtree(path)
    except FileNotFoundError:
        print("Prescript has not been run!")
        sys.exit(1)


def screenshot(data):
    with io.open(os.path.join(CURRENT_PATH, '__save', 'screenshot.json'), 'w') as context:
        context.write(json.dumps(data, indent=2))


def main():
    if len(CURRENT_PATH.split('/')) <= 2 and len(CURRENT_PATH.split("\\")) <= 2:
        raise Exception("Cannot operate out of %s" % CURRENT_PATH)
    if os.path.isdir(os.path.join(CURRENT_PATH, '__save', 'screenshot.json')) and LAZY:
        pass
    else:
        clean()  # Delete everything except the vms\
        params = {"Location": os.path.join(CURRENT_PATH, "__save", "vms")} 
        for i, param in enumerate(sys.argv):  # get params
            param = parse(i, param)
            params[param[0]] = param[1]
        for directory in params["Location"]:  # For every role in vsm that the user should've set up
            location = os.path.join(params["Location"], directory)
            solution = load_solution(location)  # load that solution
            screenshot(solution)  # let future processess know what the project looks like
            if params.get("skip_zip") != "True":  # zip the project if necessary
                package_projects(solution)


if __name__ == "__main__":
    main()
