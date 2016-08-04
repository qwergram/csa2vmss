import sys
import os
import io
import json
import pyscripts.csa_parse

CURRENT_PATH = os.getcwd()

def parse(enum, content):
    if content.startswith("-") and '=' in content:
        return (content.split('=')[0][1:], content.split('=')[1])
    else:
        return enum, content

def load_solution(params):
    parsed = pyscripts.csa_parse.VSCloudService(params['Location'])
    parsed.load_solution()
    return parsed.solution_data

def run_powershell(name, arguments):
    arguments = " ".join(["-%s \"%s\"" % (key, value) for key, value in arguments.items()])
    execute_this = "powershell -ExecutionPolicy Unrestricted -File \"%s\" %s" % (os.path.join(CURRENT_PATH, 'psscripts', name), arguments)
    print(execute_this)
    os.system(execute_this)

def package_projects(solution):
    for project in solution['projects']:
        os.mkdir(os.path.join(CURRENT_PATH, '__save', project['guid']))
        with io.open(os.path.join(CURRENT_PATH, '__save', project['guid'], "meta.json"), 'w') as f:
            f.write(json.dumps(project, indent=2))
            run_powershell("save_roles.ps1", {"zipfilename": os.path.join(CURRENT_PATH, '__save', project['guid'], "package.zip"), "sourcedir": project['folder'] + "\\" if project['folder'].endswith("\\") else project['folder']})

def clean():
    os.system('rm -r %s' % os.path.join(CURRENT_PATH, '__save'))
    os.mkdir(os.path.join(CURRENT_PATH, '__save'))

def main():
    clean()
    params = {}
    for i, param in enumerate(sys.argv):
        param = parse(i, param)
        params[param[0]] = param[1]
    solution = load_solution(params)
    zips = package_projects(solution)


if __name__ == "__main__":
    main()
