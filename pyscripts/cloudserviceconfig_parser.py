try:
    from pyscripts import util
    from pyscripts import solution_parser
except ImportError:
    import util
    import solution_parser


class CSConfigParser(object):

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

    def parse_content(self):
        pass