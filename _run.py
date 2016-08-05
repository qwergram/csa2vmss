import sys
import os
import io
import json
import pyscripts.csa_parse

CURRENT_PATH = os.getcwd()
LAZY = True


def parse(enum, content):
    if content.startswith("-") and '=' in content:
        return (content.split('=')[0][1:], content.split('=')[1])
    else:
        return enum, content


def load_solution(params):
    parsed = pyscripts.csa_parse.VSCloudService(params['Location'])
    parsed.load_solution()
    solution = parsed.solution_data
    # import pdb; pdb.set_trace()
    return solution


def run_powershell(name, arguments):
    arguments = " ".join(["-%s \"%s\"" % (key, value) for key, value in arguments.items()])
    execute_this = "powershell -ExecutionPolicy Unrestricted -File \"%s\" %s" % (os.path.join(CURRENT_PATH, 'psscripts', name), arguments)
    os.system(execute_this)


def package_projects(solution):
    for project in solution['projects']:
        project.setdefault("instances", 1)
        project.setdefault("role_type", "WorkerRole")
        os.mkdir(os.path.join(CURRENT_PATH, '__save', project['guid']))
        with io.open(os.path.join(CURRENT_PATH, '__save', project['guid'], "meta.json"), 'w') as f:
            f.write(json.dumps(project, indent=2))
            run_powershell("save_roles.ps1", {"zipfilename": os.path.join(CURRENT_PATH, '__save', project['guid'], "zip_" + project['guid'][:5] + "_package.zip"), "sourcedir": project['folder'] + "\\" if project['folder'].endswith("\\") else project['folder']})

def clean():
    os.system('rm -r %s' % os.path.join(CURRENT_PATH, '__save'))
    os.mkdir(os.path.join(CURRENT_PATH, '__save'))


def main():
    if os.path.isdir(os.path.join(CURRENT_PATH, '__save')) and LAZY:
        pass
    else:
        clean()
        params = {}
        for i, param in enumerate(sys.argv):
            param = parse(i, param)
            params[param[0]] = param[1]
        solution = load_solution(params)
        zips = package_projects(solution)


if __name__ == "__main__":
    main()
