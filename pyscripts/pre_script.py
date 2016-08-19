import io
import shutil
import sys
import os

OUTPUT = os.path.join(os.getcwd(), '__save', 'vms')

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
    build_webroles(webroles, commons)


def clean_binaries(path, strict=False):
    for to_clean in ["bin", "obj", "backup"]:
        print("Cleaning project of", to_clean)
        try:
            shutil.rmtree(os.path.join(path, to_clean))
        except FileNotFoundError as e:
            if strict:
                raise e

def build_webroles(webroles, commons):
    print("Building Web roles")
    for path, name in webroles:
        new_location = os.path.join(OUTPUT, name, name)
        print("Building", name)
        shutil.copytree(path, new_location)
        clean_binaries(new_location)
        for common in commons:
            new_common_location = os.path.join(OUTPUT, name, common[1])
            print("Copying", common[1])
            shutil.copytree(common[0], new_common_location)
            clean_binaries(new_common_location)

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

    

if __name__ == "__main__":
    main(sys.argv[1])


