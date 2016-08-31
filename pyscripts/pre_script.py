import io
import shutil
import sys
import os
try:
    from pyscripts import util
    from pyscripts import solution_parser
    from pyscripts import cloudservicedef_parser
except ImportError:
    import util
    import solution_parser
    import cloudservicedef_parser


def get_solution_data(location):
    solution = solution_parser.SolutionParser(location)
    solution.parse()
    return solution.data


def main(location):
    jsonblob = get_solution_data(location)



if __name__ == "__main__":
    params = util.parse_input()
    location = util.parse_input_args()
    if location:
        main(location)
    