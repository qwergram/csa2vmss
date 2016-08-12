import io
import os
import sys
import json

CURRENT_PATH = os.getcwd()

DEBUG = False

def debug(*args, **kwargs):
    if DEBUG:
        print("[!]", *args, **kwargs)

def load_xml(location):
    import xml.etree.ElementTree
    root = xml.etree.ElementTree.parse(location).getroot()
    return root


class VSCloudService(object):
    "A Visual Studio Object to be translated into a VMSS json template"

    guid_dir = {
        "FAE04EC0-301F-11D3-BF4B-00C04F79EFBC": "c#_project",
        "CC5FD16D-436D-48AD-A40C-5A424C6E3E79": "sln_dir",
        "2150E333-8FDC-42A3-9474-1A3956D46DE8": "powershell_project"
    }

    def __init__(self, project_path, *args, **kwargs):
        debug("Initializing VSProject")
        self.project_path = project_path
        self.solution_data = {}

    def _is_valid_project(self):
        "Check the validity of the project"
        debug("Checking if project is a VS15 project")
        # Check if it's actually a vs project
        is_vs_project = os.path.isdir(os.path.join(self.project_path, '.vs'))
        contains_sln_file = len([file for file in os.listdir(self.project_path) if file.endswith('.sln')])
        # TODO: Check for files that only appear in Cloud apps
        return is_vs_project and contains_sln_file

    def _read_sln_data(self):
        """Convert the SLN into JSON for parsing.
        Find these lines:
        Project("{CC5FD16D-436D-48AD-A40C-5A424C6E3E79}") = "ContosoAdsCloudService", "ContosoAdsCloudService\ContosoAdsCloudService.ccproj", "{0F8966AF-0D48-4840-90EF-0C8CD052FC02}"

        and grab the important data.
        """
        debug("Reading .sln file")
        sln = [file for file in os.listdir(self.project_path) if file.endswith('.sln')][0]
        sln_location = os.path.join(self.project_path, sln)
        stats = {"projects": [], "parent": {}}
        with io.open(sln_location) as sln:
            for line in sln.readlines():
                lower_line = line.lower()
                if lower_line.startswith("microsoft visual studio solution file"):
                    stats['sln_version'] = lower_line.replace('microsoft visual studio solution file, format version ', '').strip()
                elif lower_line.startswith("minimumvisualstudioversion"):
                    stats['min_vs_version'] = lower_line.split('=')[-1].strip()
                elif lower_line.startswith("visualstudioversion"):
                    stats['vs_version'] = lower_line.split('=')[-1].strip()
                elif lower_line.startswith("project("): # Parse these lines...
                    parse = line.split('\"')
                    proj_type = self.guid_dir.get(parse[1][1:-1], parse[1][1:-1])
                    if proj_type == "c#_project": # Standard csproj
                        stats['projects'].append({
                            "proj_type": {"guid": parse[1][1:-1], "type": proj_type},
                            "guid": parse[7][1:-1],
                            "folder": os.path.join(self.project_path, parse[3]),
                            "csproj": os.path.join(self.project_path, parse[5]),
                        })
                    elif proj_type == "sln_dir": # Appears to be a parent
                        stats['parent'] = self._load_ccproj_dir(parse)
                    else:
                        debug("unknown file type: [%s]" % parse[5])
                        debug("Are you sure it's a Cloud Service Project?")
                        sys.exit(1)
        return stats

    def _load_ccproj_dir(self, parse):
        """Load important files from the ccproj directory"""
        debug("Loading csdef and cscfg files")
        parent_data = {}
        parent_data['folder'] = os.path.join(self.project_path, parse[3])
        parent_data['proj_type_guid'] = "sln_dir"
        parent_data['guid'] = parse[7][1:-1]
        parent_data['ccproj'] = os.path.join(self.project_path, parse[5])
        parent_data['cscfg'] = []

        for item in os.listdir(parent_data['folder']):
            if item.endswith('csdef'):
                parent_data['csdef'] = os.path.join(parent_data['folder'], item)
            elif item.endswith('cscfg'):
                parent_data['cscfg'].append(os.path.join(parent_data['folder'], item))
        return parent_data

    def _is_valid_sln_data(self, sln_data):
        """Make sure that the data we're looking for exists"""
        debug("Checking sln data is valid")
        # TODO: Need to build some sort of verification system
        return True

    def __str__(self):
        try:
            project_count = len(self.solution_data['projects'])
            parent_location = self.solution_data['parent']['folder'].split("\\")[-1] + "\\"
        except KeyError:
            project_count = parent_location = "[NotLoaded]"
        return "<VS15Project location=\"{}\", projects={}, parent=\"{}\">".format(self.project_path, project_count, parent_location)

    @property
    def sln_json(self):
        return json.dumps(self.solution_data, indent=2, sort_keys=True)

    def json(self, *args, **kwargs):
        return {}

    def _check_solution_loaded(self):
        debug("Check solution loaded")
        return bool(self.solution_data.get('projects', False) and self.solution_data.get('parent', False))


    # XXX INCLUDE THIS SOMEHOW
    def _load_csproj(self, project_json):
        """Read xml of csproj"""
        debug("Reading xml contents")

        def mess(text):
            return "{http://schemas.microsoft.com/developer/msbuild/2003}" + text

        def clean(text):
            return text.replace("{http://schemas.microsoft.com/developer/msbuild/2003}", "")

        config_json = []
        include_json = {}
        csproj_location = project_json['csproj']
        csproj = load_xml(csproj_location)
        configurations = csproj.findall(mess("PropertyGroup"))
        include = csproj.findall(mess("ItemGroup"))
        debug("Loading PropertyGroup Data")
        for config in configurations:
            for child in config.getchildren():
                config_json.append({
                    "tag": clean(child.tag),
                    "items": {key: value for (key, value) in child.items()},
                    "text": child.text
                })
        project_json['PropertyGroups'] = config_json
        debug("Loading ItemGroup Data")
        for references in include:
            for reference in references.getchildren():
                print(clean(reference.tag), reference.items())
        return project_json

    def _load_cloud_service_defs(self):

        def clean(text):
            return text.replace("{http://schemas.microsoft.com/ServiceHosting/2008/10/ServiceDefinition}", '').lower()

        def mess(text):
            return "{http://schemas.microsoft.com/ServiceHosting/2008/10/ServiceDefinition}" + text

        parent_data = self.solution_data['parent']
        root = load_xml(parent_data['csdef'])

        for i, project in enumerate(self.solution_data['projects']):
            self.solution_data['projects'][i]['name'] = project['folder'].split("\\")[-1]

        for role in root.getchildren():
            """
            The commons file should not be treated as a role... it includes files that should be found on
            both the webrole and workerrole.. right?
            """

            attributes = {key: value for key, value in role.items()}
            # if clean(role.tag) == "WebRole":
            projectname = attributes['name']
            role_settings = {}

            for setting in role.getchildren():
                if clean(setting.tag) == "endpoints": # Spaghetti Drainer strat ftw
                    role_settings[clean(setting.tag)] = {}
                    for subset in setting.getchildren():
                        subset_items = {key: value for key, value in subset.items()}
                        role_settings[clean(setting.tag)][subset_items['name']] = {"port": subset_items['port'], "protocol": subset_items["protocol"]}
                elif clean(setting.tag) == "configurationsettings":
                    role_settings[clean(setting.tag)] = {}
                    for subset in setting.getchildren():
                        for key, value in subset.items():
                            role_settings[clean(setting.tag)][value] = None
                elif clean(setting.tag) == "sites":
                    role_settings[clean(setting.tag)] = {"bindings": []}
                    for site in setting.getchildren():
                        for bindings in site.getchildren():
                            for binding in bindings.getchildren():
                                binding = {key: value for key, value in binding.items()}
                                if binding.get('endpointName'):
                                    role_settings[clean(setting.tag)]['bindings'].append(binding['endpointName'])
                else:
                    role_settings[clean(setting.tag)] = []
                    for subset in setting.getchildren():
                        for key, value in subset.items():
                            role_settings[clean(setting.tag)].append(value)

            for i, project in enumerate(self.solution_data['projects']):
                if project['name'] == projectname:
                    self.solution_data['projects'][i]['role_type'] = clean(role.tag)
                    for key, value in role_settings.items():
                        self.solution_data['projects'][i][key.lower()] = value
                    self.solution_data['projects'][i]['vmsize'] = attributes['vmsize']
                    break

    def _load_cloud_service_configs(self):

        def clean(text):
            return text.replace("{http://schemas.microsoft.com/ServiceHosting/2008/10/ServiceConfiguration}", '')

        def mess(text):
            return "{http://schemas.microsoft.com/ServiceHosting/2008/10/ServiceConfiguration}" + text

        for config in self.solution_data['parent']['cscfg']:
            if config.lower().endswith('cloud.cscfg'):
                self.solution_data['parent']['cscfg'] = config
                break
        else:
            debug("Unable to find cloud configuration, using first file")
            self.solution_data['parent']['cscfg'] = self.solution_data['parent']['cscfg'][0]
        root = load_xml(self.solution_data['parent']['cscfg'])
        for role in root.getchildren():
            role_items = {key: value for key, value in role.items()}
            for i, project in enumerate(self.solution_data['projects']):
                if project['name'] == role_items['name']:
                    instances = int(role.find(mess("Instances")).items()[0][1])
                    self.solution_data['projects'][i]['instances'] = instances

                    for setting in role.find(mess("ConfigurationSettings")).getchildren():
                        setting = {key: value for key, value in setting.items()}
                        self.solution_data['projects'][i]['configurationsettings'][setting['name']] = setting['value']

    def _read_assembly_infos(self):
        "Read assembly files"
        for i, project in enumerate(self.solution_data['projects']):
            assembly = os.path.join(project['folder'], 'Properties', 'AssemblyInfo.cs')
            if os.path.isfile(assembly):
                with io.open(assembly, 'rb') as f:
                    assembly_content = [line.strip().decode() for line in f.readlines() if line.lower().startswith(b"[assembly:")]
                self.solution_data['projects'][i]['assembly'] = {}
                for line in assembly_content:
                    key, value = line.replace("[assembly: ", "").replace('(', " ").replace(')]', '').split(' ', 1)
                    value = value[1:-1] if value.startswith('"') and value.endswith('"') else value
                    value = False if value.lower() == "false" else value
                    value = True if type(value) == str and value.lower() == "true" else value
                    value = int(value) if type(value) == str and value.isdigit() else value
                    self.solution_data['projects'][i]['assembly'][key] = value
            else:
                self.solution_data['projects'][i]['assembly'] = None

    def _read_packages(self, package):
        packages = load_xml(package).getchildren()
        json_blob = [{key: value for key, value in package.items()} for package in packages]
        return json_blob

    def _read_appconfigs(self, config_path):
        configs = load_xml(config_path).getchildren()
        config_blob = {}
        for category in configs:
            tag = category.tag.lower()
            if tag in ["configsections", "connectionstrings"]:
                config_blob[tag] = [{key: value for key, value in setting.items()} for setting in category.getchildren()]
            elif tag in ["appsettings"]:
                config_blob[tag] = {}
                for setting in category.getchildren():
                    content = {key: value for key, value in setting.items()}
                    value = content["value"]
                    value = int(value) if value.isdigit() else value
                    value = False if type(value) == str and value.lower() == "false" else value
                    value = True if type(value) == str and value.lower() == "true" else value
                    config_blob[tag][content["key"]] = value
            # elif tag == "runtime":
                # pass
            # elif tag == "entityframework":
                # pass
            else:
                pass
        return config_blob

    def _read_package_configs(self):
        for i, project in enumerate(self.solution_data['projects']):
            folder = project['folder']
            packages = os.path.join(project['folder'], 'packages.config')
            if project.get('role_type') == 'webrole':
                appconfig = os.path.join(project['folder'], 'Web.config')
            else:
                appconfig = os.path.join(project['folder'], 'app.config')
            if os.path.isfile(packages):
                self.solution_data['projects'][i]['packageconfig_path'] = packages
                self.solution_data['projects'][i]['packages'] = self._read_packages(packages)
            if os.path.isfile(appconfig):
                self.solution_data['projects'][i]['appconfig_path'] = appconfig
                self.solution_data['projects'][i]['app_configs'] = self._read_appconfigs(appconfig)

    def _get_worker_azure_requirements(self):
        for project in self.solution_data['projects']:
            if project.get('role_type') == 'workerrole':
                print(json.dumps(project, indent=2, sort_keys=1))

    def load_solution(self):
        "Find all the configuration files"
        debug("Loading solution")
        if self._is_valid_project():
            sln_data = self._read_sln_data()
            if self._is_valid_sln_data(sln_data):
                self.solution_data = sln_data
                self._load_cloud_service_defs()
                self._load_cloud_service_configs()
                self._read_assembly_infos()
                self._read_package_configs()
                self._get_worker_azure_requirements()
            else:
                debug(".sln data invalid")
                sys.exit(1)
        else:
            debug("Not a visual studio project")
            sys.exit(1)

if __name__ == "__main__":
    solution = VSCloudService(project_path="C:\\Users\\v-nopeng\\Desktop\\C#\\")
    solution.load_solution()
    # print(solution.sln_json)
