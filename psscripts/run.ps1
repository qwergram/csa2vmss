
# These need to be params later...
Param(
    # Parameter help description
    [Parameter(Mandatory=$true)]
    [string]
    $MODE,
    [string] # The new Solution Name
    $SolutionName = "SysPrep43",
    [string] # Resource name = $ResourcePrefix + $SolutionName
    $ResourcePrefix = "ResGroup",
    [string] # storage name = $StoragePrefix + $SolutionName.ToLower()
    $StoragePrefix = "storage",
    [string] # VM prefix to mark VM related resources
    $VMPrefix = "VM",
    [string] # Location for servers
    $Location = "West US",
    [string] # Size of VM
    $SkuName = "Standard_LRS",
    [string] # container name = $containerPrefix + $SolutionName.ToLower()
    $containerPrefix = "container",
    [string] # DNS prefix to mark dns related resources
    $DNSPrefx = "dns",
    [string] # Deployment resource name
    $DeploymentPrefix = "deploy",
    [string] # script resource name
    $scriptPrefix = "script",
    [string] # Which subscription to use
    $AzureProfile = "Free Trial",
    [int] # Size in GB of VM VHD
    $VMVHDSize = 100,
    [string] # VM Size
    $VMSize = "Standard_D1",
    [string] # VM Admin username
    $VMAdmin = "Norton",
    [string] # VM Password
    $VMPassword = "SecurePassword123",
    [bool] # run app in single window?
    $singleWindow = $true
)

if ($MODE -eq "vm") {

    $PYSCRIPTS = ($pwd.Path + "\pyscripts")
    $PSSCRIPTS = ($pwd.Path + "\psscripts")

    # Have the User Login
    Write-Output "Cloud Service 2 VMss"
    Write-Output "(Send suggestions to v-nopeng@microsoft.com)"

    Try {
        $RmSubscription = Get-AzureRmSubscription -ErrorAction Stop
    } Catch {
        Write-Verbose "Please Login"
        $login = Login-AzureRmAccount
    }


    # This script parses the Visual Studio Solution and zips it

    if (Test-Path ".\__save\.confirm_a") { Write-Output "Service App already packaged" } else {
        Write-Output "Reading Cloud Service App and Packaging it"

        if ($singleWindow) {
            python ($PYSCRIPTS + "\main.py")
            if ($? -eq $false) {
                Exit
            } 
        } else {
            $result = start-process python -argument ($PYSCRIPTS + '\main.py') -Wait -PassThru
            if ($result.ExitCode -eq 1) {
                Exit
            }
        }
    }


    # Check to see if the specified ResourceGroup exists.
    Write-Output "Getting Resource Group"
    Try {
        # Get it
        $resource = Get-AzureRmResourceGroup -Name ($ResourcePrefix + $SolutionName) -Location $Location -ErrorAction Stop
    } Catch {
        Write-Output "Resource Group Does not exist. Building it."
        # If it doesn't exist, build it.
        $resource = New-AzureRmResourceGroup -Name ($ResourcePrefix + $SolutionName) -Location $Location
    }

    # Upload each of the zipped files to online storage
    Write-Output "Uploading to storage account"
    # Check that the Storage Account actually exists before uploading
    Try {
        $AzureStorage = Get-AzureRmStorageAccount -ResourceGroupName ($ResourcePrefix + $SolutionName) -Name ($StoragePrefix.ToLower() + $SolutionName.ToLower()) -ErrorAction Stop
    } Catch {
        # Built it
        Write-Output "Storage Account doesn't exist! Building it."
        $newstorage = New-AzureRmStorageAccount -ResourceGroupName ($ResourcePrefix + $SolutionName) -Name ($StoragePrefix.ToLower() + $SolutionName.ToLower()) -SkuName $SkuName -Location $Location
        $AzureStorage = Get-AzureRmStorageAccount -ResourceGroupName ($ResourcePrefix + $SolutionName) -Name ($StoragePrefix.ToLower() + $SolutionName.ToLower())
    }

    # Create a key for accessing storage
    Write-Output "Building Storage Context"
    $key = (Get-AzureRmStorageAccountKey -ResourceGroupName ($ResourcePrefix + $SolutionName) -Name ($StoragePrefix.ToLower() + $SolutionName.ToLower()))[0].Value
    $blobContext = New-AzureStorageContext -StorageAccountName ($StoragePrefix.ToLower() + $SolutionName.ToLower()) -StorageAccountKey $key


    # Build a container for it as well
    Write-Output "Building Storage container"
    Try {
        $getcontainer = Get-AzureStorageContainer -Name ($containerPrefix.ToLower() + $SolutionName.ToLower()) -Context $blobContext -ErrorAction Stop
    } Catch {
        Write-Output "Container doesn't exist! Building it."
        $newcontainer = New-AzureStorageContainer ($containerPrefix.ToLower() + $SolutionName.ToLower()) -Context $blobContext -Permission Blob
    }

    # Okay, upload the files now
    if (Test-Path -Path ".\__save\.confirm_b") { Write-Output "Files already uploaded"} else {
        Get-ChildItem ($pwd.Path + "\__save") -Exclude "cspkg", "vms", ".confirm*", "*.csv" |
        ForEach-Object {
            # Look for the zip file
            Get-ChildItem ($_.FullName + "\") -Filter "*.zip" |
            ForEach-Object {
                $upload = Set-AzureStorageBlobContent -File $_.FullName -Container ($containerPrefix.ToLower() + $SolutionName.ToLower()) -Blob $_.Name -Context $blobContext -Force

                # https://storagesysprep25.blob.core.windows.net/containersysprep25/zip_92A80_package.zip <- Should look something like this
                ("https://" + $StoragePrefix.ToLower() + $SolutionName.ToLower() + ".blob.core.windows.net/" + $containerPrefix.ToLower() + $solutionName.ToLower() + "/" + $_.Name) | Out-File -FilePath ($_.Directory.ToString() + "\blob_location.txt") -Encoding ascii
            }
        }
        "true" | Out-File -FilePath ".\__save\.confirm_b" -Encoding ascii
    }

    # Okay now build a VM for each Project
    Write-Output "Generalizing Variables"
    $Settings = ("# This is a configuration file for building a ARM Template
    storageAccountName," + $StoragePrefix.ToLower() + $SolutionName.ToLower() + $VMPrefix.ToLower() +"
    sizeOfDiskInGB," + $VMVHDSize.ToString() + "
    dataDisk1VhdName," + $VMPrefix.ToLower() + "vhd" + $SolutionName.ToLower() + "
    OSDiskName," + $VMPrefix + "os" + $SolutionName + "
    nicName," + $SolutionName + "nic
    vmName," + $VMPrefix + $SolutionName + "
    vmSize," + $VMSize)
    $Settings | Out-File ($pwd.Path + "\__save\arm_vars.csv") -Encoding ascii

    # Call the python script to actually do the generating
    Write-Output "Buildling ARM Templates (Python Script)"
    if ($singleWindow) {
        # Python Script input params: VMAdminn, VMPassword, DNSprefix
        python ($pwd.Path + "\pyscripts\generate_armt.py") $VMAdmin $VMPassword ($DNSPrefx.ToLower() + $SolutionName.ToLower())
    } else {
        # Python Script input params: VMAdminn, VMPassword, DNSprefix
        start-process python -argument (($pwd.Path + "\pyscripts\generate_armt.py") +' ' + $VMAdmin + ' ' + $VMPassword + ' ' + ($DNSPrefx.ToLower() + $SolutionName.ToLower())) -ErrorAction Stop -Wait
    }

    # Create the IIS installation
    # Resources:
    # https://blogs.msdn.microsoft.com/powershell/2014/08/07/introducing-the-azure-powershell-dsc-desired-state-configuration-extension/
    # https://msdn.microsoft.com/en-us/library/mt603660.aspx
    # https://msdn.microsoft.com/en-us/library/mt603584.aspx

    Write-Output "Uploading custom scripts to storage blob"
    Write-Output "Uploading WebRole Script"
    $uploadwebrole = Set-AzureStorageBlobContent -File ($pwd.Path + "\psscripts\webrole.ps1") -Container ($containerPrefix.ToLower() + $SolutionName.ToLower()) -Blob "webrole.ps1" -Context $blobContext -Force
    Write-Output "Uploading WorkerRole Script"
    $uploadworkerrole = Set-AzureStorageBlobContent -File ($pwd.Path + "\psscripts\workerrole.ps1") -Container ($containerPrefix.ToLower() + $SolutionName.ToLower()) -Blob "rmps.ps1" -Context $blobContext -Force


    # Build the VMs
    # Resrouces:
    # http://weblogs.asp.net/scottgu/automating-deployment-with-microsoft-web-deploy
    Write-Output "Building VMs"
    Get-ChildItem ($pwd.Path + "\__save") -Exclude '*.json', '*.csv', '*.zip', 'cspkg', 'vms', ".confirm*" |
    ForEach-Object {
        # Get the Json templates

        $foldername = $_.FullName
        $armtemplate = $null
        $paramtemplate = $null
        $zipfile = $null
        $projectid = $null

        Get-ChildItem ($foldername + "\") |
        ForEach-Object {
            if ($_.Name -eq "armtemplate.json") {
                $armtemplate = $_.FullName
                $currentProjectTemplate = Get-Content $_.FullName | ConvertFrom-Json
                $currentVmName = $currentProjectTemplate.variables.vmName
            } elseif ($_.Name -eq "armtemplate.params.json") {
                $paramtemplate = $_.FullName
            } elseif ($_.Name.Endswith('.zip')) {
                $projectid = $_.Name.Split('_')[1]
                $zipfile = $_.FullName
            } elseif ($_.Name -eq "meta.json") {
                $metadata = $_.FullName
                $currentProjectMeta = Get-Content $metadata | ConvertFrom-Json
                $currentVmRole = $currentProjectMeta.role_type.ToLower()
            }
        }

        # There should be checking to see if $armtemplate and $paramtemplate is the right file

        Write-Output ("Building " + $zipfile + " (" + $currentVmRole + ")")
        Write-Output "(This will take a while)"
        if (Test-Path -path (".\__save\.confirm_" + $currentVmName)) { Write-Output "Resource already deployed" } else {
            Write-Output "Checkout http://portal.azure.com/ to see it being deployed in live time!"
            $newdeployment = New-AzureRmResourceGroupDeployment -Name ($DeploymentPrefix + $SolutionName) -ResourceGroupName ($ResourcePrefix + $SolutionName) -TemplateFile $armtemplate -TemplateParameterFile $paramtemplate
            "true" | Out-File -FilePath (".\__save\.confirm_" + $currentVmName) -Encoding ascii
        }

        $zip_location = "https://" + $StoragePrefix.ToLower() + $SolutionName.ToLower() + ".blob.core.windows.net/" + $containerPrefix.ToLower() + $SolutionName.ToLower() + '/'

        # Enable Web Deploy ONLY if it's a Web role
        if ($currentVmRole -eq "webrole") {

            # Enable IIS, Webdeploy and Remote PowerShell
            if (Test-Path -path (".\__save\.confirm_ext_" + $currentVmName)) { Write-Output "Extension already deployed" } else {
                Write-Output "Installing Web Role components"
                $newcustomscript = Set-AzureRmVMCustomScriptExtension -ResourceGroupName ($ResourcePrefix + $SolutionName) -StorageAccountName ($StoragePrefix.ToLower() + $SolutionName.ToLower()) -ContainerName ($containerPrefix.ToLower() + $SolutionName.ToLower()) -FileName "webrole.ps1" -VMName $currentVmName -Run ("webrole.ps1 -urlcontainer " + $zip_location) -StorageAccountKey $key -Name ($scriptPrefix + $SolutionName) -Location $Location -SecureExecution
                "true" | Out-File -FilePath (".\__save\.confrim_ext_" + $currentVmName) -Encoding ascii
            }
        
        } elseif ($currentVmRole -eq "workerrole") {
            Write-Output "Installing Worker Role components"

            # Enable Remote Powershell, Download packages as well
            if (Test-Path -path (".\__save\.confirm_ext_" + $currentVmName)) { Write-Output "Extension already deployed" } else {
                $newcustomscript = Set-AzureRmVMCustomScriptExtension -ResourceGroupName ($ResourcePrefix + $SolutionName) -StorageAccountName ($StoragePrefix.ToLower() + $SolutionName.ToLower()) -ContainerName ($containerPrefix.ToLower() + $SolutionName.ToLower()) -FileName "rmps.ps1" -VMName $currentVmName -Run ("rmps.ps1 -urlcontainer " + $zip_location) -StorageAccountKey $key -Name ($scriptPrefix + $SolutionName) -Location $Location -SecureExecution
            }
        }

        # Write-Output "Deploying VMSS!"
        # # only deal with worker role for now
        # if ($currentVmRole -eq "workerroleasdf") {
            
        #     Write-Output "Stopping VM"
        #     # $stop = Stop-AzureRmVM -ResourceGroupName ($ResourcePrefix + $SolutionName) -Name $currentVmName -Force

        #     Write-Output "Marking VM as Generalized"
        #     # $mark = Set-AzureRmVm -ResourceGroupName ($ResourcePrefix + $SolutionName) -Name $currentVmName -Generalized

        #     Write-Output "Getting WorkerRole Image"
        #     # $save = Save-AzureRmVMImage -DestinationContainerName ($containerPrefix + $SolutionName.ToLower()) -Name $currentVmName -ResourceGroupName ($ResourcePrefix + $SolutionName) -VHDNamePrefix vhd -Path ($pwd.Path + "\__save\vhd.json") -Overwrite

        #     if ($singleWindow) {
        #         python ($pwd.Path + "\pyscripts\generate_vmss_armt.py") $currentVmName
        #     } else {
        #         start-process python -argument (($pwd.Path + "\pyscripts\generate_vmss_armt.py") + ' ' + $currentVmName) -ErrorAction Stop -Wait
        #     }

        #     Write-Output "Deploying VMSS"
        #     # New-AzureRmResourceGroupDeployment -Name ($DeploymentPrefix + $SolutionName) -ResourceGroupName ($ResourcePrefix + $SolutionName) -TemplateFile ($pwd.Path + "\__save\vmss_" + $currentVmName + "\vmss.json") -TemplateParameterFile ($pwd.Path + "\__save\vmss_" + $currentVmName + "\vmss.params.json")
            
        #     Write-Output "Deleting old VM"
        #     # Remove-AzureRmVM -ResourceGroupName ($ResourcePrefix + $SolutionName) -Name $currentVmName -Force
        # }

    }
} elseif ($MODE -eq "vmss") {
    Write-Output "Funny story... This doesn't actually exist yet."
}