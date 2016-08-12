# Cloud2VMSS

The point of this project is to specify a Solution directory and build Virtual Machine Scalable Sets out of it

## How to use this project

```
Powershell ./run.ps1 -SLNLocation "C:\Path\To\Project\" -VMAdmin "Norton" -VMPassword "$3cur3P@$$w0rd"
```

And it will deploy VMss required

## Params:

```
Powershell ./run.ps1
    -SLNLocation
    -VMAdmin
    -VMPassword

    [-SolutionName (Default:"SysPrep33")
    -ResourcePrefix (Default:"ResGroup")
    -StoragePrefix (Default:"storage")
    -VMPrefix (Default:"VM")
    -Location (Default:"West US")
    -SkuName (Default:"Standard_LRS")
    -containerPrefix (Default:"container")
    -DNSPrefx (Default:"dns")
    -DeploymentPrefix (Default:"deploy")
    -scriptPrefix (Default:"script")
    -AzureProfile (Default:"Free Trial")
    -VMVHDSize (Default:100)
    -VMSize (Default: Standard_D1)]
    -singleWindow (Default: false)]
```
