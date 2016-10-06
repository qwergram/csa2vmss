import util
import io

class SolutionParser(object):

    def __init__(self, sln_path):
        # Initialize SolutionParser Object
        assert util.test_path(sln_path, 'f'), sln_path
        self.path = sln_path
        self.raw_content = []
        self.data = {
            "version": None,
            "vsversion": {
                "min": None,
                "current": None
            },
            "projects": [],
            "csdef": None,
            "cscfg": None,
            "ccproj": None,
            "sln": self.path
        }

    def parse(self):
        # API sugar
        self.get_content()
        self.parse_content()

    def get_content(self):
        # Open .sln file and create list of each line
        with io.open(self.path) as context:
            self.raw_content = [[line.lower().strip(), line.strip()] for line in context.readlines()]
    
    def feed(self, content):
        # Allow user to pass in sln contents to Objects
        self.raw_content = [[line.lower().strip(), line.strip()] for line in content.split("\n") if line.strip()]

    def fetch_csdef(self, ccproj):
        # locate where the .csdef file is
        directory = util.join_path(*ccproj.split("\\")[:-1])
        for file in util.listdirpaths(directory):
            if file.lower().endswith('.csdef'):
                return file

    def fetch_cscfg(self, ccproj):
        # locate where the .cscfg file is
        directory = util.join_path(*ccproj.split("\\")[:-1])
        for file in util.listdirpaths(directory):
            if file.lower().endswith('local.cscfg'):
                return file

    def _guid_exists(self, guid):
        # Helper: make sure guid exists
        for project in self.data['projects']:
            if project['guid'] == guid:
                return True
        return False

    def parse_content(self):
        # Read self.raw_content and pass data to json blob
        for line_lower, line in self.raw_content:
            # Get SLN version data
            if line_lower.startswith("microsoft visual studio solution file"): 
                self.data['version'] = float(line_lower.replace('microsoft visual studio solution file, format version ', '').strip())
            elif line_lower.startswith("minimumvisualstudioversion"):
                self.data['vsversion']['min'] = line_lower.split('=')[-1].strip()
            elif line_lower.startswith("visualstudioversion"):
                self.data['vsversion']['current'] = line_lower.split('=')[-1].strip()
            
            elif line_lower.startswith("project("): # Parse line that starts with "project(" 
                parse = line.split('\"')
                guid = parse[7][1:-1] # Get GUID from line
                if not self._guid_exists(guid): # Check that GUID exists
                    type_guid = parse[1] # Get project type (E.g. C# or Python)
                    name = parse[3]
                    proj = parse[5]
                    location = util.join_path(*self.path.split("\\")[:-1]) # Get directory path of that project
                    
                    proj_dir = proj.split("\\")[:-1] if len(proj.split("\\")) > 1 else proj
                    if type(proj_dir) == str:
                        proj_location = location
                    else:
                        proj_location = util.join_path(location, util.join_path(*proj_dir))
                    self.data['location'] = location 
                    
                    if type_guid[1:-1] == "CC5FD16D-436D-48AD-A40C-5A424C6E3E79": # If the project type is a CS definitions project
                        self.data['cscfg'] = self.fetch_cscfg(util.join_path(location, proj)) # get CS defs/cfg/proj data
                        self.data['csdef'] = self.fetch_csdef(util.join_path(location, proj))
                        self.data['ccproj'] = util.join_path(location, proj)
                    else: # if the project is a regular project
                        self.data['projects'].append({ # Build json blob
                        "name": name,
                        "type": type_guid[1:-1],
                        "proj": util.join_path(location, proj),
                        "guid": guid,
                        "location": proj_location,
                        "ignore": False,
                    })

    def update_csdef(self, csdef):
        # Update json blob (self.data) with csdef meta data collected
        for i, project in enumerate(self.data['projects']):
            try:
                for key, value in csdef.data[project['name']].items():
                    self.data['projects'][i][key] = value
            except KeyError:
                # If project doesn't exist in csdef, it means the project isn't a role, but a dependency
                # We can ignore dependencies when building VMs
                self.data['projects'][i]["ignore"] = True

    def update_cscfg(self, cscfg):
        # Update json blob (self.data) with cscfg meta data collected
        for i, project in enumerate(self.data['projects']):
            try:
                for key, value in cscfg.data[project['name']].items():
                    self.data['projects'][i][key] = value
            except KeyError:
                # If project doesn't exist in cscfg, it means the project isn't a role, but a dependency
                # We can ignore dependencies when building VMs
                self.data['projects'][i]["ignore"] = True

    def update_proj(self, proj):
        # Update json blob (self.data) with ccproj meta data collected
        for i, project in enumerate(self.data['projects']):
            try:
                self.data['projects'][i]['references'] = [ref.upper() for ref in proj.data[project['name']]]
            except KeyError:
                # if 'project['name']' doesn't exist, there aren't any references
                self.data['projects'][i]['references'] = []
                
