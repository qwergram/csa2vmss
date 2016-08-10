
# These need to be params later...
Param(
    [string]
    $SLNLocation = "C:\\Users\\v-nopeng\\Desktop\\C#\\",
    [string]
    $SolutionName = "SysPrep32",
    [string]
    $ResourcePrefix = "ResGroup",
    [string]
    $StoragePrefix = "storage",
    [string]
    $VMPrefix = "VM",
    [string]
    $Location = "West US",
    [string]
    $SkuName = "Standard_LRS",
    [string]
    $containerPrefix = "container",
    [string]
    $DNSPrefx = "dns",
    [string]
    $DeploymentPrefix = "deploy",
    [string]
    $scriptPrefix = "script",
    [string]
    $AzureProfile = "Free Trial",
    [int]
    $VMVHDSize = 100,
    [string]
    $VMSize = "Standard_D1",
    [string]
    $VMAdmin = "titan",
    [string]
    $VMPassword = "Mar.Wed.17.2027"
)

# Virtual Machine Stats




# Visualizations for This App
$singleWindow = $false

# Have the User Login
Write-Host "Hello!"
Try {
    $RmSubscription = Get-AzureRmSubscription -ErrorAction Stop
} Catch {
    Login-AzureRmAccount
}

Try {
    $Subscription = Select-AzureSubscription $AzureProfile -ErrorAction Stop
} Catch {
    Add-AzureAccount
}

# This script parses the Visual Studio Solution and zips it
Write-Host "Reading Cloud Service App and Packaging it (Python Script)"
if ($singleWindow) {
    python _run.py ('-Location="' + $SLNLocation + '"')
} else {
    start-process python -argument ('_run.py -Location="' + $SLNLocation + '"') -Wait
}

# Check to see if the specified ResourceGroup exists.
Write-Host "Building Resource Group"
Try {
    # Get it
    Get-AzureRmResourceGroup -Name ($ResourcePrefix + $SolutionName) -Location $Location -ErrorAction Stop
} Catch {
    Write-Host "Resource Group Does not exist. Building it."
    # If it doesn't exist, build it.
    New-AzureRmResourceGroup -Name ($ResourcePrefix + $SolutionName) -Location $Location
}

# Upload each of the zipped files to online storage
Write-Host "Uploading to storage account"

# Check that the Storage Account actually exists before uploading
Try {
    $AzureStorage = Get-AzureRmStorageAccount -ResourceGroupName ($ResourcePrefix + $SolutionName) -Name ($StoragePrefix.ToLower() + $SolutionName.ToLower()) -ErrorAction Stop
} Catch {
    # Built it
    Write-Host "Storage Account doesn't exist! Building it."
    New-AzureRmStorageAccount -ResourceGroupName ($ResourcePrefix + $SolutionName) -Name ($StoragePrefix.ToLower() + $SolutionName.ToLower()) -SkuName $SkuName -Location $Location
    $AzureStorage = Get-AzureRmStorageAccount -ResourceGroupName ($ResourcePrefix + $SolutionName) -Name ($StoragePrefix.ToLower() + $SolutionName.ToLower())
}

# Create a key for accessing storage
Write-Host "Building Storage Context"
$key = (Get-AzureRmStorageAccountKey -ResourceGroupName ($ResourcePrefix + $SolutionName) -Name ($StoragePrefix.ToLower() + $SolutionName.ToLower()))[0].Value
$blobContext = New-AzureStorageContext -StorageAccountName ($StoragePrefix.ToLower() + $SolutionName.ToLower()) -StorageAccountKey $key


# Build a container for it as well
Try {
    Get-AzureStorageContainer -Name ($containerPrefix.ToLower() + $SolutionName.ToLower()) -Context $blobContext -ErrorAction Stop
} Catch {
    Write-Host "Container doesn't exist! Building it."
    New-AzureStorageContainer ($containerPrefix.ToLower() + $SolutionName.ToLower()) -Context $blobContext -Permission Blob
}

# Okay, upload the files now
Get-ChildItem ($pwd.Path + "\__save") |
ForEach-Object {
    # Look for the zip file
    if ($_.FullName.EndsWith('.csv')) {

    } else {
        Get-ChildItem ($_.FullName + "\") -Filter "*.zip" |
        ForEach-Object {
            Set-AzureStorageBlobContent -File $_.FullName -Container ($containerPrefix.ToLower() + $SolutionName.ToLower()) -Blob $_.Name -Context $blobContext -Force

            # https://storagesysprep25.blob.core.windows.net/containersysprep25/zip_92A80_package.zip <- Should look something like this
            ("https://" + $StoragePrefix.ToLower() + $SolutionName.ToLower() + ".blob.core.windows.net/" + $containerPrefix.ToLower() + $solutionName.ToLower() + "/" + $_.Name) | Out-File -FilePath ($_.Directory.ToString() + "\blob_location.txt") -Encoding ascii
        }
    }
}

# Okay now build a VM for each Project
Write-Host "Generalizing Variables"
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
Write-Host "Buildling ARM Templates (Python Script)"
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

Write-Host "Uploading custom scripts to storage blob"
Write-Host "Uploading RMPS script"
Set-AzureStorageBlobContent -File ($pwd.Path + "\psscripts\enable_rmps.ps1") -Container ($containerPrefix.ToLower() + $SolutionName.ToLower()) -Blob "rmps.ps1" -Context $blobContext -Force
Write-Host "Uploading IIS script"
Set-AzureStorageBlobContent -File ($pwd.Path + "\psscripts\enable_iis.ps1") -Container ($containerPrefix.ToLower() + $SolutionName.ToLower()) -Blob "iis.ps1" -Context $blobContext -Force
Write-Host "Uploading Web Deploy script"
Set-AzureStorageBlobContent -File ($pwd.Path + "\psscripts\enable_web_deploy.ps1") -Container ($containerPrefix.ToLower() + $SolutionName.ToLower()) -Blob "web_deploy.ps1" -Context $blobContext -Force

# Build the VMs
# Resrouces:
# http://weblogs.asp.net/scottgu/automating-deployment-with-microsoft-web-deploy
Write-Host "Building VMs"
Get-ChildItem ($pwd.Path + "\__save") -Exclude '*.*' |
ForEach-Object {
    # Get the Jon templates

    $armtemplate = $null
    $paramtemplate = $null
    $zipfile = $null
    $projectid = $null

    Get-ChildItem ($_.FullName + "\") |
    ForEach-Object {
        if ($_.Name -eq "armtemplate.json") {
            $armtemplate = $_.FullName
            $currentProjectData = Get-Content $_.FullName | ConvertFrom-Json
            $currentVmName = $currentProjectData.variables.vmName
            $currentVmRole = $currentProjectData.role_type
        } elseif ($_.Name -eq "armtemplate.params.json") {
            $paramtemplate = $_.FullName
        } elseif ($_.Name.Endswith('.zip')) {
            $projectid = $_.Name.Split('_')[1]
            $zipfile = $_.FullName
        }
    }
    # There should be checking to see if $armtemplate and $paramtemplate is the right file
    Write-Host ("Building " + $zipfile)
    New-AzureRmResourceGroupDeployment -Name ($DeploymentPrefix + $SolutionName) -ResourceGroupName ($ResourcePrefix + $SolutionName) -TemplateFile $armtemplate -TemplateParameterFile $paramtemplate

    # Enable Powershell
    Write-Host "Enabling Remote Powershell Terminal"
    Set-AzureRmVMCustomScriptExtension -ResourceGroupName ($ResourcePrefix + $SolutionName) -StorageAccountName ($StoragePrefix.ToLower() + $SolutionName.ToLower()) -ContainerName ($containerPrefix.ToLower() + $SolutionName.ToLower()) -FileName "rmps.ps1" -VMName $currentVmName -Run "rmps.ps1" -StorageAccountKey $key -Name ($scriptPrefix + $SolutionName) -Location $Location -SecureExecution
    
    
    # Enable Web Deploy ONLY if it's a Web role

    if ($currentVmRole.ToLower() -eq "webrole"){
        
        Write-Host "Installing Web Role components"

        # Enable IIS
        Write-Host "Enabling IIS"
        Set-AzureRmVMCustomScriptExtension -ResourceGroupName ($ResourcePrefix + $SolutionName) -StorageAccountName ($StoragePrefix.ToLower() + $SolutionName.ToLower()) -ContainerName ($containerPrefix.ToLower() + $SolutionName.ToLower()) -FileName "rmps.ps1" -VMName $currentVmName -Run "iis.ps1" -StorageAccountKey $key -Name ($scriptPrefix + $SolutionName) -Location $Location -SecureExecution

        # Enable Web Deploy
        Write-Host "Enabling Web Deploy"
        Set-Set-AzureRmVMCustomScriptExtension -ResourceGroupName ($ResourcePrefix + $SolutionName) -StorageAccountName ($StoragePrefix.ToLower() + $SolutionName.ToLower()) -ContainerName ($containerPrefix.ToLower() + $SolutionName.ToLower()) -FileName "rmps.ps1" -VMName $currentVmName -Run "web_deploy.ps1" -StorageAccountKey $key -Name ($scriptPrefix + $SolutionName) -Location $Location -SecureExecution


    } else {
        Write-Host "Installing Worker Role components"
    }
}
