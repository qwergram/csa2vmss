import io
import shutil
import sys
import os
from pyscripts import util, solution_parser, cloudserviceconfig_parser, cloudservicedef_parser, proj_parser
from pyscripts.runtime_tests import check_prescript

def get_solution_data(location):
    check_prescript.test_location(location)
    solution = solution_parser.SolutionParser(location)
    solution.parse()
    return solution


def get_csdef_data(solution):
    check_prescript.test_solution(solution)
    csdef = cloudservicedef_parser.CSDefinitionParser(solution)
    csdef.parse()
    return csdef


def get_cscfg_data(solution):
    check_prescript.test_solution(solution)
    cscfg = cloudserviceconfig_parser.CSConfigParser(solution)
    cscfg.parse()
    return cscfg


def get_proj_data(solution):
    check_prescript.test_solution(solution)
    proj = proj_parser.ProjParser(solution)
    proj.parse()
    return proj


def parse_solution(location):
    check_prescript.test_location(location)
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


def create_properties(guid, all_json):
    projects = []
    for project in all_json['projects']:
        if project['guid'] == guid:
            projects.append(project)
            references = project['references'] + [guid]
            i = 0
            while i < len(all_json['projects']):
                if project['guid'] in references:
                    projects.append(all_json['projects'][i])
                i += 1
            all_json['projects'] = projects
            util.save_json(all_json, util.join_path(util.SAVE_DIR, guid), 'ctv.properties')


def build_project(guid, project_json):
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

    return project_guid_json


def create_save(json_blob):
    build_save_directory()
    guid_json = get_guids(json_blob)
    for guid, project in guid_json.items():
        build_project(guid, json_blob)
        create_properties(guid, json_blob)

def main(location):
    json_blob = parse_solution(location)
    create_save(json_blob)


if __name__ == "__main__":
    params = util.parse_input()
    location = util.parse_input_args()
    if location:
        main(location)
    