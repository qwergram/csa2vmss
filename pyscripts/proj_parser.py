try:
    from pyscripts import util
    from pyscripts import solution_parser
except ImportError:
    import util
    import solution_parser
import io

class DumbXMLParser(object):

    def __init__(self, location):
        self.load(location)
    
    def load(self, location):
        with io.open(location) as context:
            self.xml = context.readlines()

    def tag_search(self, tag):
        results = []
        for i, line in enumerate(self.xml):
            if "<{}".format(tag.lower()) in line.strip().lower():
                results.append((i, line))
        return results


class ProjParser(object):

    def __init__(self, solution_data):
        if not isinstance(solution_data, solution_parser.SolutionParser):
            raise TypeError(type(solution_data))
        self.location = solution_data.data['projects']
        self.xml = None
        self.data = {}

    def parse(self):
        for i, project in enumerate(self.location):
            self.parse_one(i, project['name'])

    def parse_one(self, i, projectname):
        self.get_content(i)
        self.parse_content(projectname)

    def get_content(self, i):
        self.xml = DumbXMLParser(self.location[i]['proj'])

    def parse_content(self, projectname):
        project_refs = self.xml.tag_search("Project>")
        for ref in project_refs:
            self.data.setdefault(projectname, []).append(ref[1].replace("<Project>{", '').replace('}</Project>', '').strip())

