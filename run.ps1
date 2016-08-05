
# These need to be params later...
$SLNLocation = "C:\\Users\\v-nopeng\\Desktop\\C#\\"
$SolutionName = "SysPrep23"
$ResourcePrefix = "ResGroup"
$StoragePrefix = "storage"
$VMPrefix = "VM"
$Location = "West US"
$SkuName = "Standard_LRS"
$containerPrefix = "container"
$DNSPrefx = "dns"

# Virtual Machine Stats
$VMVHDSize = 100
$VMSize = "Standard_D1"
$VMAdmin = "titan"
$VMPassword = "Mar.Wed.17.2027"


# Visualizations for This App
$singleWindow = $false

# Have the User Login
Write-Host "Hello! Please Login"
Try {
    Get-AzureSubscription -Current -ErrorAction Stop
} Catch {
    Login-AzureRmAccount
}

# This script parses the Visual Studio Solution and zips it
Write-Host "Reading Cloud Service App and Packaging it"
if ($singleWindow) {
    python _run.py ('-Location="' + $SLNLocation + '"')
} else {
    start-process python -argument ('_run.py -Location="' + $SLNLocation + '"')
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
    Get-ChildItem ($_.FullName + "\") -Filter "*.zip" | 
    ForEach-Object {
        Set-AzureStorageBlobContent -File $_.FullName -Container ($containerPrefix.ToLower() + $SolutionName.ToLower()) -Blob $_.Name -Context $blobContext
        
    }
}

# Okay now build a VM for each Project
Write-Host "Generalizing Variables"
$Settings = ("# This is a configuration file for building a ARM Template
storageAccountName," + $StoragePrefix.ToLower() + $SolutionName.ToLower() + $VMPrefix.ToLower() +"
size," + $VMVHDSize.ToString() + "
vhdName," + $VMPrefix.ToLower() + "vhd" + $SolutionName.ToLower() + "
osdiskname," + $VMPrefix + "os" + $SolutionName + "
nicName," + $SolutionName + "nic
vmName," + $VMPrefix + $SolutionName + "
vmSize," + $VMSize)
$Settings | Out-File ($pwd.Path + "\__save\arm_vars.csv") -Encoding ascii

# Call the python script to actually do the generating
Write-Host "Buildling ARM Templates"

# input order: 
python ($pwd.Path + "\pyscripts\generate_armt.py")