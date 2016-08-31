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
    sln = SolutionParser("C:\\Windows\\explorer.exe")
    sln.feed(python_sln)
    sln.parse_content()
    assert sln.data['version'] == 12.00, sln.data
    assert sln.data['vsversion']['min'] == "10.0.40219.1"
    assert sln.data['vsversion']['current'] == "14.0.25420.1"
    assert sln.data['projects']

    