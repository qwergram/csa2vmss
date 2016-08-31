

def test_csa_init():
    from pyscripts.csa_parse import VSCloudService
    from pyscripts.util import POST_TEST_ENV
    import os
    for language in os.listdir(POST_TEST_ENV):
        for test_unit in os.path.join(POST_TEST_ENV, language):
            x = VSCloudService(project_path=os.path.join(POST_TEST_ENV, language, test_unit))
            assert x.guid_dir
            assert x.solution_data == {}
            assert x.project_path == os.path.join(POST_TEST_ENV, language, test_unit)
            assert x.write_privs
            x.write_privs = False