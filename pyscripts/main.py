import json
import os
import io
import csa_parse
import shutil

CURRENT_PATH = os.getcwd()

def save_solution_data(project_guid, data):
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


def package_solution(project_name, solution):
    project_guid = name_to_guid("ContosoAdsWeb", solution.solution_data)
    source_dir = os.path.join(CURRENT_PATH, '__save', 'vms', project_name)
    dest_dir = os.path.join(CURRENT_PATH, '__save', project_guid)
    zip_path = os.path.join(dest_dir, get_zip_guid(project_guid))
    prelim_path = os.path.join(dest_dir, 'pkg')
    for project in os.listdir(source_dir):
        project_path = os.path.join(source_dir, project)
        if os.path.isdir(project_path) and project != 'packages':
            shutil.copytree(project_path, prelim_path)


def main():
    solution = csa_parse.VSCloudService(project_path="C:\\Users\\v-nopeng\\code\\msft2016\\cstvmss\\__save\\vms\\ContosoAdsWeb\\")
    solution.load_solution()
    save_solution_data(name_to_guid("ContosoAdsWeb", solution.solution_data), solution)
    package_solution("ContosoAdsWeb", solution)

if __name__ == "__main__":
    main()