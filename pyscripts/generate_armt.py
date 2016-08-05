import sys
import os
import io
import json

CURRENT_PATH = os.getcwd()

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
    "publicIPAddressName": "myPublicIP",
    "publicIPAddressType": "Dynamic",
    "vmStorageAccountContainerName": "vhds",
    "vmName": None,
    "vmSize": None,
    "virtualNetworkName": "MyVNET",
    "vnetID": "[resourceId('Microsoft.Network/virtualNetworks', variables('virtualNetworkName'))]",
    "subnetRef": "[concat(variables('vnetID'), '/subnets/', variables('subnetName'))]"
}

with io.open(os.path.join(CURRENT_PATH, 'templates', 'iis-vm.params.json')) as content:
    PARAM_TEMPLATE = json.loads(content.read())

def load_arm_vars():
    with io.open(os.path.join(CURRENT_PATH, '__save', 'arm_vars.csv')) as content:
        new_dict = {}
        for line in content.readlines():
            if not line.strip().startswith('#'):
                key, value = line.strip().split(',')
                VARIABLES[key] = value


def create_armt_from_meta():
    with io.open(os.path.join(CURRENT_PATH, "templates", "iis-vm.json")) as content:
        content = json.loads(content.read())
    content['variables'] = VARIABLES

    PARAM_TEMPLATE['parameters']['adminUsername']['value'] = sys.argv[1]
    PARAM_TEMPLATE['parameters']['adminPassword']['value'] = sys.argv[2]
    PARAM_TEMPLATE['parameters']['dnsLabelPrefix']['value'] = sys.argv[3]


    for project in os.listdir(os.path.join(CURRENT_PATH, "__save")):
        load_arm_vars()
        project_path = os.path.join(CURRENT_PATH, '__save', project)
        if os.path.isdir(project_path):
            project_id = project[:3].lower()
            # Personalize each important variable to each project
            content['variables']['vmName'] = project_id + VARIABLES['vmName']
            content['variables']['storageAccountName'] = project_id + VARIABLES['storageAccountName']


            with io.open(os.path.join(project_path, 'armtemplate.json'), 'w') as template:
                template.write(json.dumps(content, indent=2))

            with io.open(os.path.join(project_path, 'armtemplate.params.json'), 'w') as paramtemplate:
                paramtemplate.write(json.dumps(PARAM_TEMPLATE, indent=2))


if __name__ == "__main__":
    assert len(sys.argv) == 4, len(sys.argv)
    load_arm_vars()
    create_armt_from_meta()
