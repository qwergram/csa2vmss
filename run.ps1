
# These need to be params later...
$SolutionName = "SysPrep23"
$ResourcePrefix = "ResGroup"
$StoragePrefix = "storage"
$Location = "West US"
$SkuName = "Standard_LRS"
$containerPrefix = "container"

# Have the User Login
Write-Host "Hello! Please Login"
Try {
    Get-AzureSubscription -Current -ErrorAction Stop
} Catch {
    Login-AzureRmAccount
}
# This script parses the Visual Studio Solution and zips it
Write-Host "Reading Cloud Service App and Packaging it"
python _run.py -Location="C:\\Users\\v-nopeng\\Desktop\\C#\\"

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

