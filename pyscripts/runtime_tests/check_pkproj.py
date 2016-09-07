from runtime_tests.check_prescript import test_location, test_dir_exists, test_file_exists, test_solution_json, test_guid
import util

def check_confirm_file():
    test_file_exists(util.join_path(util.SAVE_DIR, ".confirm_a"))


def check_zip_exists(zip_path):
    assert zip_path.split("\\")[-1].startswith("zip_")
    assert zip_path.split("\\")[-1].endswith(".zip")

    test_file_exists(zip_path)