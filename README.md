# Cloud2VMSS

The objective of this project is to specify a Solution directory and build Virtual Machine Scalable Sets out of it.

The point of this is to convert the existing [Paas](https://en.wikipedia.org/wiki/Platform_as_a_service) to a [Iaas](https://en.wikipedia.org/wiki/Cloud_computing#Infrastructure_as_a_service_.28IaaS.29) so developers can take advantage of
all the new technologies that come out that they wouldn't normally get using the Cloud App Service ([Paas](https://en.wikipedia.org/wiki/Platform_as_a_service))

## How to use this project

You will first need to use the pre-script to split the cloud app into seperate projects:

`python.exe .\pyscripts\pre_script.py "C:\Path\To\Project" -open`

You will then need to open each project and make sure it can run on its own.

Once you have completed that, you can run:
`Powershell ./run.ps1 -SLNLocation "C:\Path\To\Project" -VMAdmin "Norton" -VMPassword "$3cur3P@$$w0rd"`

And it will deploy a VM for each role required

## Params:

```
    python.exe .\pyscripts\pre_script.py
        <Path to project>
        [-open (If -open it will open the location of the projects in explorer)]

```


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
