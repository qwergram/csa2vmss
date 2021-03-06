import sys
import os
import io
import json
import util

PARAMETERS = {
    "adminUsername": {
        "type": "string",
        "metadata": {
            "description": "Username for the Virtual Machine."
        }
    },
    "adminPassword": {
        "type": "securestring",
        "metadata": {
            "description": "Password for the Virtual Machine."
        }
    },
    "dnsLabelPrefix": {
        "type": "string",
        "metadata": {
            "description": "Unique DNS Name for the Public IP used to access the Virtual Machine."
        }
    },
    "windowsOSVersion": {
        "type": "string",
        "defaultValue": "2012-R2-Datacenter",
        "allowedValues": [
            "2008-R2-SP1",
            "2012-Datacenter",
            "2012-R2-Datacenter"
        ],
        "metadata": {
            "description": "The Windows version for the VM. This will pick a fully patched image of this given Windows version. Allowed values: 2008-R2-SP1, 2012-Datacenter, 2012-R2-Datacenter."
        }
    }
}

VARIABLES = {
    "storageAccountName": None,
    "sizeOfDiskInGB": None,
    "dataDisk1VhdName": None,
    "imagePublisher": "MicrosoftWindowsServer",
    "imageOffer": "WindowsServer",
    "OSDiskName": None,
    "nicName": None,
    "addressPrefix": "10.0.0.0/16",
    "subnetName": "Subnet",
    "subnetPrefix": "10.0.0.0/24",
    "storageAccountType": "Standard_LRS",
    "publicIPAddressName": "publicIP",
    "publicIPAddressType": "Dynamic",
    "vmStorageAccountContainerName": "vhds",
    "vmName": None,
    "vmSize": None,
    "virtualNetworkName": "MyVNET",
    "vnetID": "[resourceId('Microsoft.Network/virtualNetworks', variables('virtualNetworkName'))]",
    "subnetRef": "[concat(variables('vnetID'), '/subnets/', variables('subnetName'))]"
}

CUSTOM_SCRIPT_PARAMS = []

PARAM_TEMPLATE = {}

PUBLIC_IP = VARIABLES['publicIPAddressName']

def load_arm_vars():
    with io.open(util.join_path(util.SAVE_DIR, 'arm_vars.csv')) as content:
        new_dict = {}
        for line in content.readlines():
            if not line.strip().startswith('#'):
                key, value = line.strip().split(',')
                VARIABLES[key] = value

def save_params_to_solution(project_name):
    with io.open(util.join_path(util.SAVE_DIR, project_name, "ctv.properties")) as context:
        solution = json.loads(context.read())

    solution['vmparams'] = {
        "username": sys.argv[1],
        "password": sys.argv[2],
        "dnslabel": sys.argv[3]
    }

    with io.open(util.join_path(util.SAVE_DIR, project_name, "ctv.properties"), 'w') as context:
        context.write(json.dumps(solution, indent=2, sort_keys=True))

def load_arm_params(project_name):
    global PARAM_TEMPLATE
    with io.open(util.templates('iis-vm.params.json')) as content:
        PARAM_TEMPLATE = json.loads(content.read())

    PARAM_TEMPLATE['parameters']['adminUsername']['value'] = sys.argv[1]
    PARAM_TEMPLATE['parameters']['adminPassword']['value'] = sys.argv[2]
    PARAM_TEMPLATE['parameters']['dnsLabelPrefix']['value'] = sys.argv[3]
    save_params_to_solution(project_name)

def create_armt_from_meta():
    with io.open(util.templates("iis-vm.json")) as content:
        content = json.loads(content.read())
    content['variables'] = VARIABLES

    for project in os.listdir(util.SAVE_DIR):
        project_path = util.join_path(util.SAVE_DIR, project)
        if os.path.isdir(project_path) and project not in ["cspkg", "vms"]:
            load_arm_vars()
            load_arm_params(project)
            project_id = project[:4].lower()
            # Personalize each important variable to each project
            content['variables']['vmName'] = project_id + VARIABLES['vmName']
            content['variables']['storageAccountName'] = project_id + VARIABLES['storageAccountName']
            content['variables']['nicName'] = project_id + VARIABLES['nicName']
            content['variables']['publicIPAddressName'] = project_id + PUBLIC_IP

            PARAM_TEMPLATE['parameters']['dnsLabelPrefix']['value'] = 'd' + project_id + PARAM_TEMPLATE['parameters']['dnsLabelPrefix']['value']

            try:
                with io.open(util.join_path(project_path, 'blob_location.txt')) as location:
                    blob_location = location.read().strip()
            except FileNotFoundError:
                continue

            CUSTOM_SCRIPT_PARAMS = ["/".join(blob_location.split('/')[:-1]), blob_location.split('/')[-1]]

            for i, resource in enumerate(content['resources']):
                if resource['name'] == "MyCustomScriptExtension":
                    content['resources'][i]['properties']['settings']['commandToExecute'] = resource['properties']['settings']['commandToExecute'].format(*CUSTOM_SCRIPT_PARAMS)
                    break

            with io.open(util.join_path(project_path, 'armtemplate.json'), 'w') as template:
                template.write(json.dumps(content, indent=2))

            with io.open(util.join_path(project_path, 'armtemplate.params.json'), 'w') as paramtemplate:
                paramtemplate.write(json.dumps(PARAM_TEMPLATE, indent=2))


if __name__ == "__main__":
    assert len(sys.argv) == 4, len(sys.argv)
    create_armt_from_meta()
