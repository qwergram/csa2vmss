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
    print(commons)


def select_commons(project_choices):
    print("\nSelect which project to be packaged with all roles (seperated by spaces)")
    for i, project in enumerate(project_choices):
        print(i, "-", project[1])
    while True:
        try:
            choice_indexes = [int(n) for n in input("Selection: ").split()]
            return [project_choices[index] for index in choice_indexes]
        except (ValueError, IndexError):
            print("Invalid selection")

    

if __name__ == "__main__":
    main(sys.argv[1])


