# http://stackoverflow.com/questions/10522240/powershell-script-to-auto-install-of-iis-7-and-above
# --------------------------------------------------------------------
# Loading Feature Installation Modules
# --------------------------------------------------------------------
Import-Module ServerManager

# --------------------------------------------------------------------
# Installing IIS
# --------------------------------------------------------------------
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
Add-WindowsFeature -Name RSAT-Web-Server -IncludeAllSubFeature
Add-WindowsFeature -Name WAS -IncludeAllSubFeature

# --------------------------------------------------------------------
# Loading IIS Modules
# --------------------------------------------------------------------
Import-Module WebAdministration


# --------------------------------------------------------------------
# Resetting IIS
# --------------------------------------------------------------------
$Command = "IISRESET"
Invoke-Expression -Command $Command


# https://blogs.technet.microsoft.com/uktechnet/2016/02/12/create-a-custom-script-extension-for-an-azure-resource-manager-vm-using-powershell/
# Ensure PS remoting is enabled, although this is enabled by default for Azure VMs
Enable-PSRemoting -Force

# Create rule in Windows Firewall
New-NetFirewallRule -Name "WinRM HTTPS" -DisplayName "WinRM HTTPS" -Enabled True -Profile Any -Action Allow -Direction Inbound -LocalPort 5986 -Protocol TCP

# Create Self Signed certificate and store thumbprint
$thumbprint = (New-SelfSignedCertificate -DnsName $env:COMPUTERNAME -CertStoreLocation Cert:\LocalMachine\My).Thumbprint

# Run WinRM configuration on command line. DNS name set to computer hostname.
$cmd = "winrm create winrm/config/Listener?Address=*+Transport=HTTPS @{Hostname=""$env:computername""; CertificateThumbprint=""$thumbprint""}"
cmd.exe /C $cmd
