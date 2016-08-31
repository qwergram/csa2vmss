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


def main(location):
    solution = get_solution_data(location)
    csdef = get_csdef_data(solution)
    cscfg = get_cscfg_data(solution)
    proj = get_proj_data(solution)
    solution.update_csdef(csdef)
    solution.update_cscfg(cscfg)
    solution.update_proj(proj)
    jsonblob = solution.data
    



if __name__ == "__main__":
    params = util.parse_input()
    location = util.parse_input_args()
    if location:
        main(location)
    