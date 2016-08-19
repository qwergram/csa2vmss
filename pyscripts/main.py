import json
import os
import csa_parse

CURRENT_PATH = os.getcwd()

def get_old_project(self):
    pass

def main():
    solution = csa_parse.VSCloudService(project_path="C:\\Users\\v-nopeng\\code\\msft2016\\cstvmss\\__save\\vms\\webrole\\")
    solution.load_solution()
    print(solution.sln_json)

if __name__ == "__main__":
    main()