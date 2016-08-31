def test_parse_input():
    from pyscripts.util import parse_input
    import sys
    sys.argv = ["file_name", "-test=test", "-key=value", "-digit=352", "-float=234.23", 
                "-bool1=true", "-bool2=false"]
    results = parse_input(defaults={"name": "Norton", 'test': "something else"})
    assert results['test'] == 'test'
    assert results['key'] == "value"
    assert results['digit'] == 352
    assert results['float'] == 234.23
    assert results['bool1'] is True
    assert results['bool2'] is False


def test_test_path():
    import os
    from pyscripts.util import test_path
    assert test_path(os.getcwd(), 'a')
    assert test_path(os.getcwd(), 'd')
    assert test_path(os.getcwd(), 'f') is False


def test_pyscripts():
    from pyscripts.util import pyscript, PYSCRIPTS
    import os
    assert pyscript("run.py") == os.path.join(PYSCRIPTS, "run.py") 
