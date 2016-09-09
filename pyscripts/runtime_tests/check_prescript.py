import util
from util import BatchTest
import requests

TEST_COUNTER = 0


def report(id, func, args):

    def send(status, id):
        try:
            requests.post("http://localost:5335/report/{1}/{0}/".format(status, id))
        except requests.exceptions.ConnectionError:
            pass

    try:
        func(*args)
        send("pass", id)
    except Exception as e:
        send("fail", id)
        raise e

def test_object(func):
    # print("Loading Test ID: {0}".format(func))
    def wrapper(func, *args):
        report(str(func), func, args)
        return func
    return wrapper


@test_object
def test_location(location):
    assert type(location) == str, location
    assert util.test_path(location, 'f')
    assert ":" in location or location.startswith("/")

@test_object
def test_solution(solution, cs_required=True):
    from solution_parser import SolutionParser
    assert type(solution) == SolutionParser
    data = solution.data
    assert type(data) == dict
    for key in ["vsversion", "projects", "cscfg", "csdef", "sln", "version"]:
        assert key in data.keys()
    assert type(data['vsversion']) == dict
    assert type(data['projects']) == list
    assert type(data['csdef']) == str and (not cs_required or len(data['csdef']) > 1), data['csdef']
    assert type(data['cscfg']) == str and (not cs_required or len(data['cscfg']) > 1), data['cscfg']
    assert type(data['sln']) == str and data['sln']
    assert type(data['version']) == float
    assert type(data['location']) == str
    for project in data['projects']:
        assert type(project) == dict
        for key, data_type in [("proj", str), ("name", str), ("type", str), ("location", str), ("guid", str), ("ignore", bool)]:
            assert key in project
            assert type(project[key]) == data_type

@test_object
def test_csdef_data(csdef):
    from cloudservicedef_parser import CSDefinitionParser
    assert type(csdef) == CSDefinitionParser
    data = csdef.data
    assert type(data) == dict
    assert len(data.keys())
    for key, value in data.items():
        assert type(key) == str
        assert type(value) == dict
        for secondary_key in ["vmsize", "role", "configurationsettings"]:
            assert secondary_key in value.keys()

@test_object
def test_cscfg_data(cscfg):
    from cloudserviceconfig_parser import CSConfigParser
    assert type(cscfg) == CSConfigParser
    data = cscfg.data
    assert type(data) == dict
    for key, value in data.items():
        assert type(key) == str
        assert type(value) == dict
        assert "instances" in value.keys()
        assert type(value['instances']) == int

@test_object
def test_proj_data(proj):
    from proj_parser import ProjParser
    assert type(proj) == ProjParser
    data = proj.data
    assert type(data) == dict
    if data.keys():
        for key, value in data.items():
            assert type(value) == list
            [test_guid(value.upper()) for value in value]
            assert type(key) == str

@test_object
def test_dir_exists(location):
    assert util.test_path(location, 'd')


@test_object
test_file_exists = test_location


@test_object
def test_solution_json(data):
    for project in data['projects']:
        assert "ignore" in project.keys()
        if project['ignore']:
            required = ["references", "name", "guid", "proj"]
        else:
            required = ["role", "vmsize", "ignore", "proj", "guid", "references", "name"]
            if project['role'].lower() == "webrole":
                for key in ["sites", "endpoints"]:
                    assert key in project.keys()
        for key in required:
            assert key in project.keys(), "{0} {1}".format(key, project.keys())
       

@test_object
def test_solution_post(solution):
    test_solution(solution)
    data = solution.data
    test_solution_json(data)


@test_object
def test_guid_json(projects):
    assert type(projects) == dict
    for key, project in projects.items():
        test_guid(key)
        assert "ignore" in project.keys()
        if project['ignore']:
            required = ["references", "name", "guid", "proj"]
        else:
            required = ["role", "vmsize", "ignore", "proj", "guid", "references", "name"]
            if project['role'].lower() == "webrole":
                for subkey in ["sites", "endpoints"]:
                    assert subkey in project.keys()
        for subkey in required:
            assert subkey in project.keys(), subkey

@test_object
def test_guid(guid):
    assert type(guid) == str
    assert guid.replace('-', '').isalnum()
    assert guid.upper() == guid

@test_object
def test_properties_exists(all_json, path):
    import io, json
    assert type(path) == str
    assert type(all_json) == dict
    properties = util.join_path(path, 'ctv.properties')
    assert util.test_path(properties, 'f')
    with io.open(properties) as context:
        blob = json.loads(context.read())
    assert type(blob) == dict
    assert len(all_json['projects']) >= len(blob['projects'])
    assert len(blob['projects'])
    assert path.split("\\")[-1] == blob['projects'][0]['guid']
    if blob['projects'][0]['references'] == []:
        assert len(blob['projects']) == 1


@test_object
def test_guid_exists(guid, project_json):
    test_guid(guid)
    test_solution_json(project_json)
    for item in project_json['projects']:
        if item['guid'] == guid:
            break
    else:
        assert False, guid + " not in project_json"


@test_object
def test_sln(sln_location, guids):
    import io
    from proj_parser import ProjParser
    from solution_parser import SolutionParser
    assert util.test_path(sln_location, "f")
    assert sln_location.endswith(".sln")
    assert type(guids) == list
    [test_guid(guid) for guid in guids]
    y = SolutionParser(sln_location)
    y.parse()
    y.data['csdef'] = "somestring"
    y.data['cscfg'] = "somestring"
    y.data['ccproj'] = "somestring"
    test_solution(y)
    x = ProjParser(y)
    x.parse()
    test_proj_data(x)
