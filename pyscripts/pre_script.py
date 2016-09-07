import io
import util, solution_parser, cloudserviceconfig_parser, cloudservicedef_parser, proj_parser
from runtime_tests import check_prescript

def get_solution_data(location):
    # Tests Included (9/6/16)
    check_prescript.test_location(location)
    solution = solution_parser.SolutionParser(location)
    solution.parse()
    check_prescript.test_solution(solution)
    return solution


def get_csdef_data(solution):
    # Tests Included (9/6/16)
    check_prescript.test_solution(solution)
    csdef = cloudservicedef_parser.CSDefinitionParser(solution)
    csdef.parse()
    check_prescript.test_csdef_data(csdef)
    return csdef


def get_cscfg_data(solution):
    # Tests Included (9/6/16)
    check_prescript.test_solution(solution)
    cscfg = cloudserviceconfig_parser.CSConfigParser(solution)
    cscfg.parse()
    check_prescript.test_cscfg_data(cscfg)
    return cscfg


def get_proj_data(solution):
    # Tests Included (9/6/16)
    check_prescript.test_solution(solution)
    proj = proj_parser.ProjParser(solution)
    proj.parse()
    check_prescript.test_proj_data(proj)
    return proj


def parse_solution(location):
    # Tests Included (9/6/16)
    check_prescript.test_location(location)
    solution = get_solution_data(location)
    csdef = get_csdef_data(solution)
    cscfg = get_cscfg_data(solution)
    proj = get_proj_data(solution)
    solution.update_csdef(csdef)
    solution.update_cscfg(cscfg)
    solution.update_proj(proj)

    check_prescript.test_csdef_data(csdef)
    check_prescript.test_cscfg_data(cscfg)
    check_prescript.test_proj_data(proj)
    check_prescript.test_solution_post(solution)
    return solution.data


def get_guids(json_blob, all=False):
    # Tests Included (9/6/16)
    check_prescript.test_solution_json(json_blob)
    projects = {}
    for project in json_blob['projects']:
        if (project['ignore'] is False) or all:
            projects[project['guid']] = project
    check_prescript.test_guid_json(projects)
    return projects


def create_properties(guid, all_json):
    # Tests Included (9/6/16)
    check_prescript.test_guid(guid)
    check_prescript.test_solution_json(all_json)
    all_json = all_json.copy()
    projects = []
    for project in all_json['projects']:
        if project['guid'] == guid:
            projects.append(project)
            references = project['references']
            i = 0
            while i < len(all_json['projects']):
                if project['guid'] in references:
                    projects.append(all_json['projects'][i])
                i += 1
            all_json['projects'] = projects
            util.save_json(all_json, util.join_path(util.SAVE_DIR, guid), 'ctv.properties')
            break
    check_prescript.test_properties_exists(all_json, util.join_path(util.SAVE_DIR, guid))


def build_project(guid, project_json):
    # Tests Included (9/6/16)
    check_prescript.test_guid(guid)
    check_prescript.test_solution_json(project_json)
    check_prescript.test_guid_exists(guid, project_json)

    util.mkdir(util.SAVE_DIR, guid)
    project_guid_json = get_guids(project_json, all=True)
    this_project = project_guid_json[guid]
    references = this_project['references']
    if references:
        util.copytree(this_project['location'], util.join_path(util.SAVE_DIR, guid, this_project['name']))
        for reference in references:
            util.copytree(project_guid_json[reference]['location'], util.join_path(util.SAVE_DIR, guid, project_guid_json[reference]['name']))
    else:
        util.copytree(this_project['location'], util.join_path(util.SAVE_DIR, guid))
    create_sln([guid] + references, project_guid_json, nest=len(references))

    check_prescript.test_dir_exists(util.join_path(util.SAVE_DIR, guid))
    check_prescript.test_file_exists(util.join_path(util.SAVE_DIR, guid, "{0}.sln".format(guid)))
    return project_guid_json


def create_sln(guids, json_blob, nest):
    # Tests Included (9/7/16)
    assert type(guids) == list, guids
    assert len(guids) > 0, guids
    check_prescript.test_dir_exists(util.join_path(util.SAVE_DIR, guids[0]))

    [check_prescript.test_guid(guid) for guid in guids]
    check_prescript.test_guid_json(json_blob)
    template = """Project("{0}") = "{1}", "{2}", "{3}"\nEndProject\n"""""
    initial_string = """Microsoft Visual Studio Solution File, Format Version 12.00\n# Visual Studio 14\nVisualStudioVersion = 14.0.25420.1\nMinimumVisualStudioVersion = 10.0.40219.1\n"""
    for guid in guids:
        assert guid == json_blob[guid]['guid']
        type_guid = json_blob[guid]['type']
        name = json_blob[guid]['name']
        proj = json_blob[guid]['proj'].split("\\")[-1]
        if nest:
            initial_string += template.format("{" + type_guid + "}", name, util.join_path(name, proj), "{" + guid + "}")
        else:
            initial_string += template.format("{" + type_guid + "}", name, proj, "{" + guid + "}")
    with io.open(util.join_path(util.SAVE_DIR, guids[0], "{0}.sln".format(guids[0])), 'w') as context:
        context.write(initial_string)
    check_prescript.test_sln(util.join_path(util.SAVE_DIR, guids[0], "{0}.sln".format(guids[0])), guids)

def create_save(json_blob):
    # Tests Included (9/6/16)
    check_prescript.test_solution_json(json_blob)
    util.mkdir(util.SAVE_DIR)
    guid_json = get_guids(json_blob)
    for guid in guid_json.keys():
        build_project(guid, json_blob)
        create_properties(guid, json_blob)

def main(location):
    # Tests Included (9/6/16)
    check_prescript.test_location(location)
    check_prescript.test_location(location)
    json_blob = parse_solution(location)
    create_save(json_blob)


if __name__ == "__main__":
    params = util.parse_input()
    location = util.parse_input_args()
    if location:
        main(location[0])
    