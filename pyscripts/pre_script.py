import io
import shutil
import sys
import os

OUTPUT = os.path.join(os.getcwd(), '__save', 'vms')

def make_save():
    try:
        try:
            os.mkdir(os.path.join(os.getcwd(), '__save'))
        except FileExistsError:
            shutil.rmtree(os.path.join(os.getcwd(), '__save'))
            os.mkdir(os.path.join(os.getcwd(), '__save'))
    except PermissionError:
        print("\n\nInvalid Permissions. Try running as an administrator?")
        sys.exit(1)

def main(solution_path):
    print("A tool to seperate the Project into seperate directories")
    project_choices = []
    for directory in os.listdir(solution_path):
        path = os.path.join(solution_path, directory)
        if os.path.isdir(path) and (directory.lower() not in ['backup', '.vs', 'packages']):
            project_choices.append((path, directory))
    project_choices.append('.')
    commons = select_commons(project_choices)
    webroles = select_webroles(project_choices, commons)
    workerroles = select_workerroles(project_choices, commons + webroles)
    build_roles(webroles, commons, "Web")
    build_roles(workerroles, commons, "Worker")
    save_project_directory(solution_path)


def save_project_directory(path):
    print("Saving Source under .source")
    with io.open(os.path.join(OUTPUT, ".source"), 'w') as context:
        context.write(path)


def clean_binaries(path, strict=False):
    for to_clean in ["bin", "obj", "backup", "env"]:
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


def write_confirm(location):
    try:
        os.remove(os.path.join(location, '.errors'))
    except FileNotFoundError:
        pass
    with io.open(os.path.join(location, ".confirm"), 'w') as context:
        context.write("true")


def check():
    print("\nChecking to see if build was succesful")
    for directory in os.listdir(OUTPUT):
        path = os.path.join(OUTPUT, directory)
        if os.path.isfile(path):
            continue
        clean_binaries(path)
        sln_file = os.path.join(path, [f for f in os.listdir(path) if f.lower().endswith('.sln')][0])
        # This is only specific to my computer, I think. I need to build some kind of searcher for the MSBuild
        # or at least ask for user input
        output = os.popen("%windir%\\Microsoft.NET\\Framework64\\v4.0.30319\\MSBuild.exe \"{}\"".format(sln_file)).read()
        if "0 Error(s)" in output:
            write_confirm(path)
            with io.open(os.path.join(path, '.log'), 'w') as context:
                context.write(output)
            print("Compiled", directory)
        else:
            with io.open(os.path.join(path, ".errors"), 'w') as context:
                context.write(output)
            print("Error compiling", directory, "\nError Message saved in .errors")


def check_db_strings():
    print("Checking your db strings")
    proper_db_string_in_all = True
    for project in os.listdir(OUTPUT):
        proper_db_string = True
        project_path = os.path.join(OUTPUT, project)
        if os.path.isdir(project_path):
            local = os.path.join(project_path, '.parent', 'ServiceConfiguration.Local.cscfg')
            cloud = os.path.join(project_path, '.parent', 'ServiceConfiguration.Cloud.cscfg')
            with io.open(local) as context:
                proper_db_string = not 'value="UseDevelopmentStorage=true"' in context.read() and proper_db_string
            with io.open(cloud) as context:
                proper_db_string = not 'value="UseDevelopmentStorate=true"' in context.read() and proper_db_string
        if not proper_db_string:
            print("Your connection strings aren't configured properly. Please check", project + "\\.parent\\ServiceConfiguration.*.cscfg and edit the ServiceConfiguration > Role > ConfigurationSettings > Setting'")
            print("Compile check will not be run until this is resolved.")
            print("To override this, read the README.md")
            proper_db_string_in_all = False
    return proper_db_string_in_all


def get_parent():
    print("Getting Parent")
    with io.open(os.path.join(OUTPUT, ".source")) as context:
        path = context.read().strip()
    for project in os.listdir(path) + [path]:
        project_path = os.path.join(path, project)
        if os.path.isdir(project_path):
            csdef = len([f for f in os.listdir(project_path) if f.lower().endswith(".csdef")]) >= 1
            cscfg = len([f for f in os.listdir(project_path) if f.lower().endswith(".cscfg")]) >= 1
            if csdef and cscfg:
                return project_path
    print("Parent not found. Does it contain a .csdef and .cscfg file?")
    sys.exit(1)


def copy_parent(parent_path):
    print("Copying Parent to each vm instance")
    for vm in os.listdir(OUTPUT):
        vm_path = os.path.join(OUTPUT, vm)
        if os.path.isdir(vm_path):
            print("Copying to", vm)
            try:
                os.mkdir(os.path.join(vm_path, '.parent'))
            except FileExistsError:
                print("Parent already exists, skipping.")
                continue
            for file in os.listdir(parent_path):
                path = os.path.join(parent_path, file)
                if file.lower().split('.')[-1] in ('ccproj', 'user', 'cscfg', 'csdef'):
                    shutil.copy(path, os.path.join(vm_path, ".parent"))
                elif os.path.isdir(path) and file == "bin":
                    shutil.copytree(path, os.path.join(vm_path, '.parent', 'bin'))
    print("If the cloud service app is already in the vm directory, delete `.parent`")
    print("When you made the adjustments you need, run this again with `-updatesln`")


def update_sln():
    print("Updating .SLNs")
    for vm in os.listdir(OUTPUT):
        print("Updating sln of", vm)
        path = os.path.join(OUTPUT, vm)
        parent_path = os.path.join(path, '.parent')
        if os.path.isfile(parent_path): continue
        if os.path.isfile(path): continue
        if os.path.isdir(parent_path):
            sln = [os.path.join(path, sln) for sln in os.listdir(path) if sln.endswith('.sln')][0]
            ccproj = [ccproj for ccproj in os.listdir(parent_path) if ccproj.endswith('.ccproj')][0]
            with io.open(sln) as context:
                sln_contents = context.read()
            parent_project_string = '\nProject("{CC5FD16D-436D-48AD-A40C-5A424C6E3E79}") = ".parent", ".parent\%s", "{AAAAAAAA-BBBB-CCCC-DDDD-EEEEEEEEEEEE}"\nEndProject\n' % ccproj
            sln_contents = sln_contents.replace("\nGlobal", parent_project_string + "Global")
            with io.open(sln, 'w') as context:
                context.write(sln_contents)
        else:
            print("No custom parent found in", path)
            print("You will need to launch Visual Studio again and add .parent as an existing project")


if __name__ == "__main__":
    try:
        if not sys.argv[1].startswith("-"):
            make_save()
            main(sys.argv[1])
    except IndexError:
        print("You need to pass in at least one parameter")
        print("(or -clear, -check, -cscopy, -updatesln, -open)")
        sys.exit(1)
    if "-clear" in sys.argv:
        print("Clearing .\\__save\\vms\\")
        try:
            try:
                shutil.rmtree(os.path.join(OUTPUT, ''))
            except OSError:
                shutil.rmtree(os.path.join(OUTPUT, ''))
        except FileNotFoundError:
            print("Already cleared!")
    if "-check" in sys.argv:
        if check_db_strings() or "-ignoredb" in sys.argv:
            check()
    if "-cscopy" in sys.argv:
        parent = get_parent()
        copy_parent(parent)
    if "-updatesln" in sys.argv:
        update_sln()
        print("You are now read to run `main.cmd -mode vm`")
    # Always open the directory last
    if "-open" in sys.argv:
        os.system("explorer.exe " + OUTPUT)
