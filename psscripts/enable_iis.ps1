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
