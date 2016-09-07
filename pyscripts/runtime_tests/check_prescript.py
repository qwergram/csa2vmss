import util
from util import BatchTest

def test_location(location):
    assert type(location) == str, location
    assert util.test_path(location, 'f')
    assert ":" in location or location.startswith("/")


def test_solution(solution):
    from solution_parser import SolutionParser
    assert type(solution) == SolutionParser
    data = solution.data
    assert type(data) == dict
    for key in ["vsversion", "projects", "cscfg", "csdef", "sln", "version"]:
        assert key in data.keys()
    assert type(data['vsversion']) == dict
    assert type(data['projects']) == list
    assert type(data['csdef']) == str
    assert type(data['cscfg']) == str
    assert type(data['sln']) == str
    assert type(data['version']) == float
    assert type(data['location']) == str
    for project in data['projects']:
        assert type(project) == dict
        for key, data_type in [("proj", str), ("name", str), ("type", str), ("location", str), ("guid", str), ("ignore", bool)]:
            assert key in project
            assert type(project[key]) == data_type


def test_csdef_data(csdef):
    from cloudservicedef_parser import CSDefinitionParser
    assert type(csdef) == CSDefinitionParser
    data = csdef.data
    assert type(data) == dict
    for key, value in data.items():
        assert type(key) == str
        assert type(value) == dict
        for secondary_key in ["vmsize", "role", "configurationsettings"]:
            assert secondary_key in value.keys()


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


def test_proj_data(proj):
    from proj_parser import ProjParser
    assert type(proj) == ProjParser
    data = proj.data
    assert type(data) == dict
    print("REQUIRES MORE PROJ TESTS")


def test_dir_exists(location):
    assert util.test_path(location, 'd')


def test_solution_json(data):
    for project in data['projects']:
        for key in ["role", "vmsize", "ignore", "proj", "guid", "references", "name", "ignore"]:
            assert key in project.keys()
        if project['role'].lower() == "webrole":
            for key in ["sites", "endpoints"]:
                assert key in project.keys()


def test_solution_post(solution):
    test_solution(solution)
    data = solution.data
    test_solution_json(data)


def test_guid_json(projects):
    assert type(projects) == dict
    for key, project in projects.items():
        test_guid(key)
        for subkey in ["role", "vmsize", "ignore", "proj", "guid", "references", "name", "ignore"]:
            assert subkey in project.keys()
        if project['role'].lower() == "webrole":
            for subkey in ["sites", "endpoints"]:
                assert subkey in project.keys()

def test_guid(guid):
    assert type(guid) == str
    assert guid.replace('-', '').isalnum()
    assert guid.upper() == guid


def test_properties_exists(all_json, path):
    import io, json
    assert type(path) == str
    assert type(all_json) == dict
    properties = util.join_path(path, 'ctv.properties')
    assert util.test_path(properties, 'f')
    with io.open(properties) as context:
        blob = json.loads(context.read())
    assert type(blob) == dict
    import pdb; pdb.set_trace()