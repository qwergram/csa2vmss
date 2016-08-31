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

    def mess(self, text):
        return "{http://schemas.microsoft.com/ServiceHosting/2008/10/ServiceConfiguration}" + text

    def parse_content(self):
        xml_data = {}
        for role in self.xml.getchildren():
            role_items = {key: value for key, value in role.items()}
            rolename = role_items['name']
            del role_items['name']
            xml_data[rolename] = role_items
            instances = int(role.find(self.mess("Instances")).items()[0][1])
            xml_data[rolename]['instances'] = instances
            for setting in role.find(self.mess("ConfigurationSettings")).getchildren():
                setting = {key: value for key, value in setting.items()}
                try:
                    xml_data[rolename]['configurationsettings'][setting['name']] = setting['value']
                except KeyError:
                    xml_data[rolename]['configurationsettings'] = {setting['name']: setting['value']}
        self.data = xml_data