import io
import shutil
import sys
import os
try:
    from pyscripts import util
    from pyscripts import solution_parser
    from pyscripts import cloudservicedef_parser
    from pyscripts import cloudserviceconfig_parser
    from pyscripts import proj_parser
except ImportError:
    import util
    import solution_parser
    import cloudservicedef_parser
    import cloudserviceconfig_parser
    import proj_parser


def get_solution_data(location):
    solution = solution_parser.SolutionParser(location)
    solution.parse()
    return solution


def get_csdef_data(solution):
    csdef = cloudservicedef_parser.CSDefinitionParser(solution)
    csdef.parse()
    return csdef


def get_cscfg_data(solution):
    cscfg = cloudserviceconfig_parser.CSConfigParser(solution)
    cscfg.parse()
    return cscfg


def get_proj_data(solution):
    proj = proj_parser.ProjParser(solution)
    proj.parse()
    return proj


def parse_solution(location):
    solution = get_solution_data(location)
    csdef = get_csdef_data(solution)
    cscfg = get_cscfg_data(solution)
    proj = get_proj_data(solution)
    solution.update_csdef(csdef)
    solution.update_cscfg(cscfg)
    solution.update_proj(proj)
    return solution.data


def build_save_directory():
    if not util.test_path(util.SAVE_DIR, 'd'):
        util.mkdir(util.SAVE_DIR)
    if not util.test_path(util.VMPATH):
        util.mkdir(util.VMPATH)


def get_guids(json_blob, all=False):
    projects = {}
    for project in json_blob['projects']:
        if (project['ignore'] is False) or all:
            projects[project['guid']] = project
    return projects


def build_project(guid, project_json):
    util.mkdir(util.SAVE_DIR, guid)

    project_json = get_guids(project_json, all=True)
    this_project = project_json[guid]
    references = this_project['references']
    if references:
        util.copytree(this_project['location'], util.join_path(util.SAVE_DIR, guid, this_project['name']))
        for reference in references:
            util.copytree(project_json[reference]['location'], util.join_path(util.SAVE_DIR, guid, project_json[reference]['name']))
    else:
        util.copytree(this_project['location'], util.join_path(util.SAVE_DIR, guid))

    return project_json


def create_save(json_blob):
    build_save_directory()
    guid_json = get_guids(json_blob)
    for guid, project in guid_json.items():
        build_project(guid, json_blob)


def main(location):
    json_blob = parse_solution(location)
    create_save(json_blob)

    



if __name__ == "__main__":
    params = util.parse_input()
    location = util.parse_input_args()
    if location:
        main(location)
    