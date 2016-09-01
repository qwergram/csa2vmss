python_sln = """Microsoft Visual Studio Solution File, Format Version 12.00
# Visual Studio 14
VisualStudioVersion = 14.0.25420.1
MinimumVisualStudioVersion = 10.0.40219.1
Project("{CC5FD16D-436D-48AD-A40C-5A424C6E3E79}") = "FaceAPI", "FaceAPI.ccproj", "{FA30B932-2CE6-414E-B3B7-8C028448A100}"
EndProject
Project("{888888A0-9F3D-457C-B088-3A5042F75D52}") = "FaceAPIWebRole", "FaceAPIWebRole\FaceAPIWebRole.pyproj", "{02BD14C6-B33A-4676-85A8-075CCF0AB7FC}"
EndProject
Project("{888888A0-9F3D-457C-B088-3A5042F75D52}") = "FaceAPIWorkerRole", "FaceAPIWorkerRole\FaceAPIWorkerRole.pyproj", "{3130CF5E-BA53-4129-A5C2-ECC9ACC3D73F}"
EndProject
Global
	GlobalSection(SolutionConfigurationPlatforms) = preSolution
		Debug|Any CPU = Debug|Any CPU
		Release|Any CPU = Release|Any CPU
	EndGlobalSection
	GlobalSection(ProjectConfigurationPlatforms) = postSolution
		{FA30B932-2CE6-414E-B3B7-8C028448A100}.Debug|Any CPU.ActiveCfg = Debug|Any CPU
		{FA30B932-2CE6-414E-B3B7-8C028448A100}.Debug|Any CPU.Build.0 = Debug|Any CPU
		{FA30B932-2CE6-414E-B3B7-8C028448A100}.Release|Any CPU.ActiveCfg = Release|Any CPU
		{FA30B932-2CE6-414E-B3B7-8C028448A100}.Release|Any CPU.Build.0 = Release|Any CPU
		{02BD14C6-B33A-4676-85A8-075CCF0AB7FC}.Debug|Any CPU.ActiveCfg = Debug|Any CPU
		{02BD14C6-B33A-4676-85A8-075CCF0AB7FC}.Debug|Any CPU.Build.0 = Debug|Any CPU
		{02BD14C6-B33A-4676-85A8-075CCF0AB7FC}.Release|Any CPU.ActiveCfg = Release|Any CPU
		{02BD14C6-B33A-4676-85A8-075CCF0AB7FC}.Release|Any CPU.Build.0 = Release|Any CPU
		{3130CF5E-BA53-4129-A5C2-ECC9ACC3D73F}.Debug|Any CPU.ActiveCfg = Debug|Any CPU
		{3130CF5E-BA53-4129-A5C2-ECC9ACC3D73F}.Debug|Any CPU.Build.0 = Debug|Any CPU
		{3130CF5E-BA53-4129-A5C2-ECC9ACC3D73F}.Release|Any CPU.ActiveCfg = Release|Any CPU
		{3130CF5E-BA53-4129-A5C2-ECC9ACC3D73F}.Release|Any CPU.Build.0 = Release|Any CPU
	EndGlobalSection
	GlobalSection(SolutionProperties) = preSolution
		HideSolutionNode = FALSE
	EndGlobalSection
EndGlobal"""


def test_solution_parser_feed():
    from pyscripts.solution_parser import SolutionParser
    sln = SolutionParser("C:\\Windows\\explorer.exe")
    sln.feed(python_sln)
    assert len(sln.raw_content) == len(python_sln.split("\n"))
    assert sln.raw_content[0][1] == "Microsoft Visual Studio Solution File, Format Version 12.00"
    assert sln.raw_content[0][0] == "Microsoft Visual Studio Solution File, Format Version 12.00".lower()
    line = []
    line.append('Project("{888888A0-9F3D-457C-B088-3A5042F75D52}") = "FaceAPIWorkerRole", "FaceAPIWorkerRole\FaceAPIWorkerRole.pyproj", "{3130CF5E-BA53-4129-A5C2-ECC9ACC3D73F}"'.lower())
    line.append('Project("{888888A0-9F3D-457C-B088-3A5042F75D52}") = "FaceAPIWorkerRole", "FaceAPIWorkerRole\FaceAPIWorkerRole.pyproj", "{3130CF5E-BA53-4129-A5C2-ECC9ACC3D73F}"')
    assert line in sln.raw_content
    assert len([line_lower for line_lower, line in sln.raw_content if line_lower.startswith("microsoft visual studio solution file")])


def test_solution_parser_feed_content():
    from pyscripts.solution_parser import SolutionParser
    sln = SolutionParser("C:\\Users\\v-nopeng\\code\\msft2016\\FaceAPI\\FaceAPI.sln")
    sln.feed(python_sln)
    sln.parse_content()
    assert sln.data['version'] == 12.00, sln.data
    assert sln.data['vsversion']['min'] == "10.0.40219.1"
    assert sln.data['vsversion']['current'] == "14.0.25420.1"
    assert sln.data['projects'][0]['name'] == "FaceAPIWebRole"
    assert sln.data['projects'][0]['type'] == "888888A0-9F3D-457C-B088-3A5042F75D52"
    assert sln.data['projects'][0]['proj'] == "C:\\Users\\v-nopeng\\code\\msft2016\\FaceAPI\\FaceAPIWebRole\\FaceAPIWebRole.pyproj"
    assert sln.data['projects'][0]['location'] == "C:\\Users\\v-nopeng\\code\\msft2016\\FaceAPI\\FaceAPIWebRole"
    assert sln.data['projects'][0]['guid'] == "02BD14C6-B33A-4676-85A8-075CCF0AB7FC"
    assert sln.data['location'] == "C:\\Users\\v-nopeng\\code\\msft2016\\FaceAPI"
    assert sln.data['sln'] == "C:\\Users\\v-nopeng\\code\\msft2016\\FaceAPI\\FaceAPI.sln"
    assert sln.data['csdef'] == "C:\\Users\\v-nopeng\\code\\msft2016\\FaceAPI\\ServiceDefinition.csdef"
    assert sln.data['cscfg'] == "C:\\Users\\v-nopeng\\code\\msft2016\\FaceAPI\\ServiceConfiguration.Local.cscfg"
    assert sln.data['ccproj'] == "C:\\Users\\v-nopeng\\code\\msft2016\\FaceAPI\\FaceAPI.ccproj"


def test_solution_parser_parse():
    from pyscripts.solution_parser import SolutionParser
    sln = SolutionParser("C:\\Users\\v-nopeng\\code\\msft2016\\FaceAPI\\FaceAPI.sln")
    sln.parse()
    assert sln.data['version'] == 12.00, sln.data
    assert sln.data['vsversion']['min'] == "10.0.40219.1"
    assert sln.data['vsversion']['current'] == "14.0.25420.1"
    assert sln.data['projects'][0]['name'] == "FaceAPIWebRole"
    assert sln.data['projects'][0]['type'] == "888888A0-9F3D-457C-B088-3A5042F75D52"
    assert sln.data['projects'][0]['proj'] == "C:\\Users\\v-nopeng\\code\\msft2016\\FaceAPI\\FaceAPIWebRole\\FaceAPIWebRole.pyproj"
    assert sln.data['projects'][0]['location'] == "C:\\Users\\v-nopeng\\code\\msft2016\\FaceAPI\\FaceAPIWebRole"
    assert sln.data['projects'][0]['guid'] == "02BD14C6-B33A-4676-85A8-075CCF0AB7FC"
    assert sln.data['location'] == "C:\\Users\\v-nopeng\\code\\msft2016\\FaceAPI"
    assert sln.data['sln'] == "C:\\Users\\v-nopeng\\code\\msft2016\\FaceAPI\\FaceAPI.sln"
    assert sln.data['csdef'] == "C:\\Users\\v-nopeng\\code\\msft2016\\FaceAPI\\ServiceDefinition.csdef"
    assert sln.data['cscfg'] == "C:\\Users\\v-nopeng\\code\\msft2016\\FaceAPI\\ServiceConfiguration.Local.cscfg"
    assert sln.data['ccproj'] == "C:\\Users\\v-nopeng\\code\\msft2016\\FaceAPI\\FaceAPI.ccproj"


def test_prescript_parse_solution():
    from pyscripts.pre_script import get_solution_data
    from pyscripts.solution_parser import SolutionParser
    sln2 = SolutionParser("C:\\Users\\v-nopeng\\code\\msft2016\\FaceAPI\\FaceAPI.sln")
    sln2.parse()
    sln = get_solution_data("C:\\Users\\v-nopeng\\code\\msft2016\\FaceAPI\\FaceAPI.sln")
    assert sln.data == sln2.data


def test_csdefp_get_content():
    from pyscripts.pre_script import get_solution_data
    from pyscripts.cloudservicedef_parser import CSDefinitionParser
    sln = get_solution_data("C:\\Users\\v-nopeng\\code\\msft2016\\FaceAPI\\FaceAPI.sln")
    csdef = CSDefinitionParser(sln)
    csdef.get_content()
    assert csdef.xml


def test_csdefp_parse_content():
    from pyscripts.pre_script import get_solution_data
    from pyscripts.cloudservicedef_parser import CSDefinitionParser
    sln = get_solution_data("C:\\Users\\v-nopeng\\code\\msft2016\\FaceAPI\\FaceAPI.sln")
    csdef = CSDefinitionParser(sln)
    csdef.parse()
    assert csdef.data['FaceAPIWebRole']['vmsize'] == 'Small'
    assert csdef.data['FaceAPIWebRole']['role'] == 'webrole'


def test_prescript_parse_csdef():
    from pyscripts.pre_script import get_csdef_data, get_solution_data
    sln = get_solution_data("C:\\Users\\v-nopeng\\code\\msft2016\\FaceAPI\\FaceAPI.sln")
    csdef = get_csdef_data(sln)
    assert csdef.data['FaceAPIWebRole']['vmsize'] == 'Small'
    assert csdef.data['FaceAPIWebRole']['role'] == 'webrole'
    


def test_proj_parser_get_content():
    from pyscripts.proj_parser import ProjParser
    from pyscripts.pre_script import get_solution_data
    sln = get_solution_data("C:\\Users\\v-nopeng\\code\\msft2016\\FaceAPI\\FaceAPI.sln")
    proj = ProjParser(sln)
    proj.get_content(0)
    assert isinstance(proj.xml.xml, list)


def test_proj_parser_parse_one():
    from pyscripts.proj_parser import ProjParser
    from pyscripts.pre_script import get_solution_data
    sln = get_solution_data("C:\\Users\\v-nopeng\\code\\msft2016\\FaceAPI\\FaceAPI.sln")
    proj = ProjParser(sln)
    proj.parse_one(0, 'FaceAPIWebRole')
    assert isinstance(proj.xml.xml, list)
    assert proj.data == {}
    

def test_proj_parser_parse_one_2():
    from pyscripts.proj_parser import ProjParser
    from pyscripts.pre_script import get_solution_data
    sln = get_solution_data("C:\\Users\\v-nopeng\\code\\msft2016\\Contoso\\ContosoAdsCloudService.sln")
    proj = ProjParser(sln)
    proj.parse_one(0, 'ContosoAdsWeb')
    assert isinstance(proj.xml.xml, list)
    assert proj.data['ContosoAdsWeb'] == ["4362fc53-98e5-4e46-98a1-1f99ad74c13b", "9c837457-68c0-4b86-8cac-69f9b560d0d8"]


def test_solution_update_csdef():
    from pyscripts.pre_script import get_solution_data, get_csdef_data
    sln = get_solution_data("C:\\Users\\v-nopeng\\code\\msft2016\\Contoso\\ContosoAdsCloudService.sln")
    csdef = get_csdef_data(sln)
    sln.update_csdef(csdef)
    assert sln.data['projects'][0]['role'] == 'webrole'
    assert sln.data['projects'][0]['vmsize'] == 'Small'
    assert sln.data['projects'][0]['ignore'] is False, sln.data['projects'][0]['name'] 


def test_solution_update_csdef_py():
    from pyscripts.pre_script import get_solution_data, get_csdef_data
    sln = get_solution_data("C:\\Users\\v-nopeng\\code\\msft2016\\FaceAPI\\FaceAPI.sln")
    csdef = get_csdef_data(sln)
    sln.update_csdef(csdef)
    assert sln.data['projects'][0]['role'] == 'webrole'
    assert sln.data['projects'][0]['vmsize'] == 'Small'
    assert sln.data['projects'][0]['ignore'] is False, sln.data['projects'][0]['name'] 
    assert len(sln.data['projects']) == 2


def test_solution_update_cscfg():
    from pyscripts.pre_script import get_solution_data, get_cscfg_data, get_csdef_data
    sln = get_solution_data("C:\\Users\\v-nopeng\\code\\msft2016\\Contoso\\ContosoAdsCloudService.sln")
    csdef = get_csdef_data(sln)
    sln.update_csdef(csdef)
    cscfg = get_cscfg_data(sln)
    assert cscfg.data is not None
    sln.update_cscfg(cscfg)
    
    assert sln.data['projects'][0]['role'] == 'webrole'
    assert sln.data['projects'][0]['vmsize'] == 'Small'
    assert sln.data['projects'][0]['instances'] == 1
    assert sln.data['projects'][0]['ignore'] is False, sln.data['projects'][0]['name'] 

def test_solution_update_proj():
    from pyscripts.pre_script import get_solution_data, get_cscfg_data, get_csdef_data, get_proj_data
    sln = get_solution_data("C:\\Users\\v-nopeng\\code\\msft2016\\Contoso\\ContosoAdsCloudService.sln")
    csdef = get_csdef_data(sln)
    sln.update_csdef(csdef)
    assert sln.data['projects'][0]['ignore'] is False, sln.data['projects'][0]['name'] 
    assert sln.data['projects'][1]['ignore'] is False, sln.data['projects'][1]['name'] 
    assert sln.data['projects'][2]['ignore'], sln.data['projects'][2]['name'] 
    cscfg = get_cscfg_data(sln)
    sln.update_cscfg(cscfg)
    assert sln.data['projects'][0]['ignore'] is False, sln.data['projects'][0]['name'] 
    assert sln.data['projects'][1]['ignore'] is False, sln.data['projects'][1]['name'] 
    assert sln.data['projects'][2]['ignore'], sln.data['projects'][2]['name']
    proj = get_proj_data(sln)
    sln.update_proj(proj)
    assert sln.data['projects'][0]['ignore'] is False, sln.data['projects'][0]['name'] 
    assert sln.data['projects'][1]['ignore'] is False, sln.data['projects'][1]['name'] 
    assert sln.data['projects'][2]['ignore'], sln.data['projects'][2]['name'] 

    assert sln.data['projects'][0]['role'] == 'webrole'
    assert sln.data['projects'][0]['vmsize'] == 'Small'
    assert sln.data['projects'][0]['instances'] == 1
    assert sln.data['projects'][0]['references'] == ['4362fc53-98e5-4e46-98a1-1f99ad74c13b'.upper(), '9c837457-68c0-4b86-8cac-69f9b560d0d8'.upper()]
    assert len(sln.data['projects']) == 3


def test_solution_update_proj_py():
    from pyscripts.pre_script import get_solution_data, get_cscfg_data, get_csdef_data, get_proj_data
    sln = get_solution_data("C:\\Users\\v-nopeng\\code\\msft2016\\FaceAPI\\FaceAPI.sln")
    csdef = get_csdef_data(sln)
    sln.update_csdef(csdef)
    cscfg = get_cscfg_data(sln)
    sln.update_cscfg(cscfg)
    proj = get_proj_data(sln)
    sln.update_proj(proj)

    assert sln.data['projects'][0]['role'] == 'webrole'
    assert sln.data['projects'][0]['vmsize'] == 'Small'
    assert sln.data['projects'][0]['instances'] == 1
    assert sln.data['projects'][0]['references'] == []
    assert len(sln.data['projects']) == 2
    assert sln.data['projects'][0]['ignore'] is False, sln.data['projects'][0]['name'] 
    assert sln.data['projects'][1]['ignore'] is False, sln.data['projects'][1]['name'] 


def test_create_get_guids_py():
    from pyscripts.pre_script import get_guids, parse_solution
    py_json_blob = parse_solution("C:\\Users\\v-nopeng\\code\\msft2016\\FaceAPI\\FaceAPI.sln")
    py_json_guids = get_guids(py_json_blob)

    assert "02BD14C6-B33A-4676-85A8-075CCF0AB7FC" in py_json_guids.keys()
    assert "3130CF5E-BA53-4129-A5C2-ECC9ACC3D73F" in py_json_guids.keys()
    assert len(py_json_guids.keys()) == 2


def test_get_guids_cs():
    from pyscripts.pre_script import get_guids, parse_solution
    cs_json_blob = parse_solution("C:\\Users\\v-nopeng\\code\\msft2016\\Contoso\\ContosoAdsCloudService.sln")
    cs_json_guids = get_guids(cs_json_blob)

    assert "92A8015A-1CCC-4527-B890-F604A2E764ED" in cs_json_guids.keys()
    assert "9C837457-68C0-4B86-8CAC-69F9B560D0D8" in cs_json_guids.keys()
    assert len(cs_json_guids.keys()) == 2


def test_build_project_cs():
    from pyscripts.pre_script import build_project, get_guids, parse_solution
    from pyscripts import util
    cs_json_blob = parse_solution("C:\\Users\\v-nopeng\\code\\msft2016\\Contoso\\ContosoAdsCloudService.sln")
    result = build_project(cs_json_blob['projects'][0]['guid'], cs_json_blob)
    assert util.test_path("C:\\Users\\v-nopeng\\code\\msft2016\\cstvmss\\__save\\" + cs_json_blob['projects'][0]['guid'] + "\\ContosoAdsWeb", 'd')
    assert util.test_path("C:\\Users\\v-nopeng\\code\\msft2016\\cstvmss\\__save\\" + cs_json_blob['projects'][0]['guid'] + "\\ContosoAdsCommon", 'd')
    assert len(list(util.listdirpaths("C:\\Users\\v-nopeng\\code\\msft2016\\cstvmss\\__save\\" + cs_json_blob['projects'][0]['guid']))) == 3  