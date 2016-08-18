Param(
    [Parameter(Mandatory=$true)]
    [string]
    $urlcontainer
)

# https://blogs.technet.microsoft.com/uktechnet/2016/02/12/create-a-custom-script-extension-for-an-azure-resource-manager-vm-using-powershell/
# Ensure PS remoting is enabled, although this is enabled by default for Azure VMs
Enable-PSRemoting -Force

# Create rule in Windows Firewall
Try {
    Get-NetFirewallRule -Name "WinRM HTTPS" -ErrorAction Stop
} Catch {
    New-NetFirewallRule -Name "WinRM HTTPS" -DisplayName "WinRM HTTPS" -Enabled True -Profile Any -Action Allow -Direction Inbound -LocalPort 5986 -Protocol TCP
}

# Create Self Signed certificate and store thumbprint
$thumbprint = (New-SelfSignedCertificate -DnsName $env:COMPUTERNAME -CertStoreLocation Cert:\LocalMachine\My).Thumbprint

# Run WinRM configuration on command line. DNS name set to computer hostname.
$cmd = "winrm create winrm/config/Listener?Address=*+Transport=HTTPS @{Hostname=""$env:computername""; CertificateThumbprint=""$thumbprint""}"
cmd.exe /C $cmd

# http://stackoverflow.com/questions/10522240/powershell-script-to-auto-install-of-iis-7-and-above
# --------------------------------------------------------------------
# Loading Feature Installation Modules
# --------------------------------------------------------------------
Import-Module ServerManager

# --------------------------------------------------------------------
# Installing IIS
# --------------------------------------------------------------------
Add-WindowsFeature -Name Web-Server -IncludeAllSubFeature
Add-WindowsFeature -Name Web-Common-Http -IncludeAllSubFeature
Add-WindowsFeature -Name Web-Asp-Net -IncludeAllSubFeature
Add-WindowsFeature -Name Web-Net-Ext -IncludeAllSubFeature
Add-WindowsFeature -Name Web-ISAPI-Ext -IncludeAllSubFeature
Add-WindowsFeature -Name Web-ISAPI-Filter -IncludeAllSubFeature
Add-WindowsFeature -Name Web-Http-Logging -IncludeAllSubFeature
Add-WindowsFeature -Name Web-Request-Monitor -IncludeAllSubFeature
Add-WindowsFeature -Name Web-Basic-Auth -IncludeAllSubFeature
Add-WindowsFeature -Name Web-Windows-Auth -IncludeAllSubFeature
Add-WindowsFeature -Name Web-Filtering -IncludeAllSubFeature
Add-WindowsFeature -Name Web-Performance -IncludeAllSubFeature
Add-WindowsFeature -Name Web-Mgmt-Console -IncludeAllSubFeature
Add-WindowsFeature -Name Web-Mgmt-Compat -IncludeAllSubFeature
Add-WindowsFeature -Name WAS -IncludeAllSubFeature


# --------------------------------------------------------------------
# Loading IIS Modules
# --------------------------------------------------------------------
Import-Module WebAdministration


# --------------------------------------------------------------------
# Resetting IIS
# --------------------------------------------------------------------
Invoke-Expression -Command "IISRESET"

# Enable Web Deploy on remote server
# http://www.iis.net/learn/publish/using-web-deploy/use-the-web-deployment-tool

Invoke-WebRequest -Uri http://go.microsoft.com/fwlink/?LinkId=255386 -OutFile WebInstaller.msi
Invoke-WebRequest -Uri http://go.microsoft.com/fwlink/?LinkID=309497 -OutFile installer.msi
Invoke-WebRequest -Uri http://go.microsoft.com/fwlink/?LinkId=209116 -OutFile wmsvc.msi

msiexec /i WebInstaller.msi /quiet
msiexec /i installer.msi /quiet ADDLOCAL=ALL
msiexec /i wmsvc.msi /quiet ADDLOCAL=ALL

cmd.exe /c '"%programfiles%\microsoft\web platform installer\WebpiCmd.exe" /Install /Products:ManagementService'
cmd.exe /c "net start msdepsvc"
cmd.exe /c "net start wmsvc"

$scripts_location = '%programfiles%\IIS\Microsoft Web Deploy v2\Scripts\'
$zipName = ("zip_" + $env:COMPUTERNAME.Substring(0, 4).ToUpper() + "_package.zip")

Invoke-WebRequest -Uri ($urlcontainer + $zipName) -OutFile project.zip

Add-Type -AssemblyName System.IO.Compression.FileSystem
[System.IO.Compression.ZipFile]::ExtractToDirectory("project.zip", "C:\webrole\")
