# Cloud2VMSS

The objective of this project is to specify a Solution directory and build Virtual Machine Scalable Sets out of it.

The point of this is to convert the existing [Paas](https://en.wikipedia.org/wiki/Platform_as_a_service) to a [Iaas](https://en.wikipedia.org/wiki/Cloud_computing#Infrastructure_as_a_service_.28IaaS.29) so developers can take advantage of
all the new technologies that come out that they wouldn't normally get using the Cloud App Service ([Paas](https://en.wikipedia.org/wiki/Platform_as_a_service))

# Run Prescript

First, run `prescript.cmd C:\path\to\project` to prepare your solution under `__save\<project guid>\`.

Open each of the projects in Visual Studio and make sure you're able to get the projects running locally

# Run Main

Once everything works locally, run `main.cmd -mode vm` to upload all your projects to VMs.

# RDC in the Remote VMs

Use the RDC files created by the tool and login into your VMs and make sure that your roles will run
after restarts. Once you're done with those steps, on the remote machine run `C:\sysprepme.cmd`.

# Run Main Again

Once you're finished, run `main.cmd -mode vmss` to turn the VMs into VMSSs.