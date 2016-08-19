import io
import shutil
import sys
import os

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


def get_user_choice(project_choices):
    while True:
        try:
            choice_indexes = [int(n) for n in input("Selection: ").split()]
            return [project_choices[index] for index in choice_indexes]
        except (ValueError, IndexError):
            print("Invalid selection")


def select_workerroles(project_choices, ignore):
    print("\nSelect which project are worker roles (seperated by spaces)")
    for i, choice in enumerate(project_choices):
        if choice not in ignore:
            print(i, "-", choice[1])
    return get_user_choice(project_choices)


def select_webroles(project_choices, ignore):
    print("\nSelect which project are web roles (seperated by spaces)")
    for i, choice in enumerate(project_choices):
        if choice not in ignore:
            print(i, "-", choice[1])
    return get_user_choice(project_choices)

def select_commons(project_choices):
    print("\nSelect which project to be packaged with all roles (seperated by spaces)")
    for i, project in enumerate(project_choices):
        print(i, "-", project[1])
    return get_user_choice(project_choices)

    

if __name__ == "__main__":
    main(sys.argv[1])


