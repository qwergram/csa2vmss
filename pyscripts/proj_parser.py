try:
    from pyscripts import util
    from pyscripts import solution_parser
except ImportError:
    import util
    import solution_parser

class DumbXMLParser(object):

    def __init__(self, location):
        self.load(location)
    
    def load(self, location):
        with io.open(location) as context:
            self.xml = context.readlines()

    def tag_search(self, tag):
        for line in self.xml:
            if "<{}".format(tag.lower()) in line.strip().lower():
                return line



class ProjParser(object):

    def __init__(self, solution_data):
        if not isinstance(solution_data, solution_parser.SolutionParser):
            raise TypeError(type(solution_data))
        self.location = solution_data.data['cscfg']
        self.xml = None
        self.data = None

    def parse(self):
        self.get_content()
        self.parse_content()

    def get_content(self):
        self.xml = util.load_xml(self.location)

    def mess(self, text):
        return "{http://schemas.microsoft.com/ServiceHosting/2008/10/ServiceConfiguration}" + text

    def parse_content(self):
        pass