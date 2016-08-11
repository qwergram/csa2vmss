# Enable Web Deploy on remote server
# http://www.iis.net/learn/publish/using-web-deploy/use-the-web-deployment-tool

Invoke-WebRequest -Uri http://go.microsoft.com/fwlink/?LinkID=309497 -OutFile installer.msi
msiexec /i ./installer.msi /quiet ADDLOCAL=ALL