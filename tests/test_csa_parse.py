def get_test_units():
    from pyscripts.csa_parse import VSCloudService
    from pyscripts.util import list_vms
    for unit in list_vms():
        x = VSCloudService(project_path=unit[1])
        assert x.project_path == unit[1]
        x.write_privs = False
        yield x

def test_csa_init():
    for test_unit in get_test_units():
        assert test_unit.guid_dir
        assert test_unit.solution_data == {}
        assert test_unit.write_privs is False

def test_csa__get_sln_path():
    from pyscripts.util import VMPATH
    for test_unit in get_test_units():
        assert test_unit._get_sln_path().endswith('.sln')
        assert VMPATH in test_unit._get_sln_path()


def test_csa__get_sln_contents():
    for test_unit in get_test_units():
        assert "Microsoft Visual Studio Solution File" in str(test_unit._get_sln_contents(test_unit._get_sln_path()))


def test_csa__is_valid_solution():
    from pyscripts.csa_parse import VSCloudService
    from pyscripts.util import POST_TEST_ENV
    for test_unit in get_test_units():
        sln_data = test_unit._read_sln_data()
