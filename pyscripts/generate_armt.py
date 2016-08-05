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
    "storageAccountType": None,
    "publicIPAddressName": None,
    "publicIPAddressType": "Dynamic",
    "vmStorageAccountContainerName": "vhds",
    "vmName": None,
    "vmSize": None,
    "virtualNetworkName": None,
    "vnetID": "[resourceId('Microsoft.Network/virtualNetworks', variables('virtualNetworkName'))]",
    "subnetRef": "[concat(variables('vnetID'), '/subnets/', variables('subnetName'))]"
}

def create_armt_from_meta():
    pass
