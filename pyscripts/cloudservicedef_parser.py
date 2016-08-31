try:
    from pyscripts import util
    from pyscripts import solution_parser
except ImportError:
    import util
    import solution_parser
import io


def clean_xml_tag(text):
    return text.replace("{http://schemas.microsoft.com/ServiceHosting/2008/10/ServiceDefinition}", '').lower()


class CSDefinitionParser(object):

    def __init__(self, solution_data):
        if not isinstance(solution_data, solution_parser.SolutionParser):
            raise TypeError(type(solution_data))
        self.location = solution_data.data['csdef']
        self.xml = None


    def parse(self):
        pass


    def get_content(self):
        self.xml = util.load_xml(self.location)


    def parse_content(self):
        for role in self.xml.getchildren():
            role_settings = {}
            for setting in role.getchildren():
                if clean_xml_tag(setting.tag) == "endpoints":
                    role_settings[clean_xml_tag(setting.tag)] = {}
                    for subset in setting.getchildren():
                        subset_items = {key: value for key, value in subset.items()}
                        role_settings[clean_xml_tag(setting.tag)][subset_items['name']] = {"port": subset_items['port'], "protocol": subset_items["protocol"]}
                elif clean_xml_tag(setting.tag) == "configurationsettings":
                    role_settings[clean_xml_tag(setting.tag)] = {}
                    for subset in setting.getchildren():
                        for key, value in subset.items():
                            role_settings[clean_xml_tag(setting.tag)][value] = None
                elif clean_xml_tag(setting.tag) == "sites":
                    role_settings[clean_xml_tag(setting.tag)] = {"bindings": []}
                    for site in setting.getchildren():
                        for bindings in site.getchildren():
                            for binding in bindings.getchildren():
                                binding = {key: value for key, value in binding.items()}
                                if binding.get('endpointName'):
                                    role_settings[clean_xml_tag(setting.tag)]['bindings'].append(binding['endpointName'])
                else:
                    role_settings[clean_xml_tag(setting.tag)] = []
                    for subset in setting.getchildren():
                        for key, value in subset.items():
                            role_settings[clean_xml_tag(setting.tag)].append(value)