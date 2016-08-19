import io
import shutil
import sys
import os

OUTPUT = os.path.join(os.getcwd(), '__save', 'vms')

def make_save():
    try:
        os.mkdir(os.path.join(os.getcwd(), '__save'))
    except FileExistsError:
        shutil.rmtree(os.path.join(os.getcwd(), '__save'))
        os.mkdir(os.path.join(os.getcwd(), '__save'))

def main(solution_path):
    print("A tool to seperate the Project into seperate directories")
    project_choices = []
    for directory in os.listdir(solution_path):
        path = os.path.join(solution_path, directory)
        if os.path.isdir(path) and (directory.lower() not in ['backup', '.vs', 'packages']):
            project_choices.append((path, directory))
    commons = select_commons(project_choices)
    webroles = select_webroles(project_choices, commons)
    workerroles = select_workerroles(project_choices, commons + webroles)
    build_roles(webroles, commons, "Web")
    build_roles(workerroles, commons, "Worker")


def clean_binaries(path, strict=False):
    for to_clean in ["bin", "obj", "backup"]:
        print("Cleaning project of", os.path.join(path, to_clean))
        try:
            shutil.rmtree(os.path.join(path, to_clean))
        except FileNotFoundError as error:
            if strict:
                raise error

def copy_sln(src, dest, required_solutions):
    required_solutions = [sln[1] for sln in required_solutions]
    sln_name = [f for f in os.listdir(src) if f.lower().endswith('.sln')][0]
    src = os.path.join(src, sln_name)
    dest_sln = os.path.join(dest, sln_name)

    print("Reading solution document")
    with io.open(src) as context:
        solution_file = context.readlines()
    
    blacklist_keys = []
    print("Transforming solution document")
    for i, line in enumerate(solution_file):
        line_lower = line.lower()
        if line_lower.startswith("project("):
            project_guid = line.split('"')[-2][1:-1]
            project_name = line.split("= \"")[1].split("\",", 1)[0]
            if project_name not in required_solutions:
                blacklist_keys.append(project_guid)
                blacklist_keys.append(project_name)
        for key in blacklist_keys:
            if key in line:
                solution_file[i] = ''
    solution = "".join(solution_file).replace("EndProject\nEndProject", "EndProject")
    
    print("Writing solution document")
    with io.open(dest_sln, 'w') as context:
        context.write(solution)

    print("Leaving a nice message :)")
    with io.open(os.path.join(dest, "README.md"), 'w') as context:
        context.write("""# Tasks:
- Open the project in visual studio and edit it as neccesary
- When done, you can run the main script
## Things to keep in mind:
- The Cloud Service App Paradigm no longer applies here. So don't use it.
""")


def build_roles(roles, commons, mode):
    print("Building", mode, "roles")
    for path, name in roles:
        new_location = os.path.join(OUTPUT, name, name)
        print("Building", name)
        shutil.copytree(path, new_location)
        clean_binaries(new_location)
        for common in commons:
            new_common_location = os.path.join(OUTPUT, name, common[1])
            print("Copying", common[1])
            shutil.copytree(common[0], new_common_location)
            clean_binaries(new_common_location)
        copy_sln("\\".join(path.split("\\")[:-1]), os.path.join(OUTPUT, name), roles + commons)
        

def get_user_choice(project_choices, auto=None):
    while True:
        try:
            if not auto:
                choice_indexes = [int(n) for n in input("Selection: ").split()]
            else:
                choice_indexes = auto
            return [project_choices[index] for index in choice_indexes]
        except (ValueError, IndexError):
            print("Invalid selection")


def select_workerroles(project_choices, ignore):
    print("\nSelect which project are worker roles (seperated by spaces)")
    for i, choice in enumerate(project_choices):
        if choice not in ignore:
            print(i, "-", choice[1])
    return get_user_choice(project_choices, [4])


def select_webroles(project_choices, ignore):
    print("\nSelect which project are web roles (seperated by spaces)")
    for i, choice in enumerate(project_choices):
        if choice not in ignore:
            print(i, "-", choice[1])
    return get_user_choice(project_choices, [3])


def select_commons(project_choices):
    print("\nSelect which project to be packaged with all roles (seperated by spaces)")
    for i, project in enumerate(project_choices):
        print(i, "-", project[1])
    return get_user_choice(project_choices, [1, 2])

def write_confirm(location):
    with io.open(os.path.join(location, ".confirm"), 'w') as context:
        context.write("true")


def check():
    print("\nChecking to see if build was succesful")
    for directory in os.listdir(OUTPUT):
        path = os.path.join(OUTPUT, directory)
        clean_binaries(path)
        sln_file = os.path.join(path, [f for f in os.listdir(path) if f.lower().endswith('.sln')][0])
        errors = os.system("%windir%\\Microsoft.NET\\Framework64\\v4.0.30319\\MSBuild.exe \"{}\"".format(sln_file))
        if not errors:
            write_confirm(path)
        else:
            print("Error compiling", directory)


if __name__ == "__main__":
    make_save()
    main(sys.argv[1])
    try:
        if "-open" in sys.argv:
            os.system("explorer.exe " + OUTPUT)
        elif "-check" in sys.argv:
            check()

    except IndexError:
        pass


