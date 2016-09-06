from pyscripts import util
from pyscripts.util import BatchTest

def test_location(location):
    assert type(location) == str
    assert util.test_path(location)
    assert ":" in location or location.startswith("/")


def test_solution(solution):
    from pyscripts.solution_parser import SolutionParser
    assert type(solution) == SolutionParser
    