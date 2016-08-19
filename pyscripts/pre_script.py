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


def select_commons(project_choices):
    print("\nSelect which project to be packaged with all roles (seperated by spaces)")
    for i, project in enumerate(project_choices):
        print(i, "-", project[1])

if __name__ == "__main__":
    main(sys.argv[1])


