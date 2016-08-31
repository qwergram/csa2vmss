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
        self.data = None


    def parse(self):
        self.get_content()
        self.parse_content()


    def get_content(self):
        self.xml = util.load_xml(self.location)


    def parse_content(self):
        xml_data = {}
        for role in self.xml.getchildren():
            attributes = {key: value for key, value in role.items()}
            projectname = attributes['name']
            del attributes['name']
            xml_data[projectname] = {key: value for key, value in role.items()}
            xml_data[projectname]['role'] = clean_xml_tag(role.tag)
            for setting in role.getchildren():
                if clean_xml_tag(setting.tag) == 'endpoints':
                    xml_data[projectname]['endpoints'] = {}
                    for subset in setting.getchildren():
                        subset_items = {key: value for key, value in subset.items()}
                        xml_data[projectname]['endpoints'][subset_items['name']] = {
                            "port": subset_items['port'], 
                            "protocol": subset_items["protocol"]
                        }
                elif clean_xml_tag(setting.tag) == "configurationsettings":
                    xml_data[projectname]["configurationsettings"] = {}
                    for subset in setting.getchildren():
                        for key, value in subset.items():
                            xml_data[projectname]["configurationsettings"][key] = value
                elif clean_xml_tag(setting.tag) == "sites":
                    xml_data[projectname]["sites"] = {"bindings": []}
                    for site in setting.getchildren():
                        for bindings in site.getchildren():
                            for binding in bindings.getchildren():
                                binding = {key: value for key, value in binding.items()}
                                if binding.get('endpointName'):
                                    xml_data[projectname]["sites"]['bindings'].append(binding['endpointName'])
        self.data = xml_data
