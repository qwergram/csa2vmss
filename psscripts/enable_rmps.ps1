# https://blogs.technet.microsoft.com/uktechnet/2016/02/12/create-a-custom-script-extension-for-an-azure-resource-manager-vm-using-powershell/
# Ensure PS remoting is enabled, although this is enabled by default for Azure VMs
Param(
    [Parameter(Mandatory=$true)]
    [string]
    $urlcontainer
)

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


# Download the package for this worker role
$zipName = ("zip_" + $env:COMPUTERNAME.Substring(0, 4).ToUpper() + "_package.zip")
Invoke-WebRequest -Uri ($urlcontainer + $zipName) -OutFile project.zip

Add-Type -AssemblyName System.IO.Compression.FileSystem
[System.IO.Compression.ZipFile]::ExtractToDirectory("project.zip", "C:\workerrole")
$schedule_task = "schtasks /create /XML C:\workerrole\scheduler.xml /tn workerrole_bootstrap"
$run_task = "schtasks /run /tn workerrole_bootstrap"
cmd.exe /C $schedule_task
cmd.exe /C $run_task

# cmd.exe /C "%windir%\System32\Sysprep\sysprep.exe /quiet /shutdown /generalize /audit"