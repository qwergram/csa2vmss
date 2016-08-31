import azure
from pyscripts import util


DEFAULTS = {
    "solutionName": "SP55",
    "resourcePrefix": "RG",
    "storagePrefix": "stg",
    "VMPrefix": "VM",
    "Location": "West US",
    "SkuName": "Standard_LRS",
    "containerPrefix": "container",
    "DNSPrefix": "dns",
    "DeploymentPrefix": "deploy",
    "scriptPrefix": "scrpt",
    "VMVHDSize": 100,
    "VMSize": "Standard_D1",
    "VMAdmin": "Norton",
    "VMPassword": "SecurePassword123!"
}


def main(params):
    pass



if __name__ == "__main__":
    PARAMS = util.parse_input(DEFAULTS)
    main(PARAMS)