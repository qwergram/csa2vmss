# Cloud2VMSS

NOTE: THIS PROJECT IS NOT COMPLETE YET

The objective of this project is to specify a Solution directory and build Virtual Machine Scalable Sets out of it.

The point of this is to convert the existing [Paas](https://en.wikipedia.org/wiki/Platform_as_a_service) to a [Iaas](https://en.wikipedia.org/wiki/Cloud_computing#Infrastructure_as_a_service_.28IaaS.29) so developers can take advantage of
all the new technologies that come out that they wouldn't normally get using the Cloud App Service ([Paas](https://en.wikipedia.org/wiki/Platform_as_a_service))

# How to use this project

## Using the Prescript to prime the project

Note: If you need to ever restart from scratch use the command ```prescript.cmd -clear```
Note: Make sure that the directory name matches the role name defined in the .sln

### Copying the directories over

You will first need to use the pre-script to split the cloud app into seperate projects:

```prescript.cmd "C:\Path\To\Project\Directory" -open -cscopy```

-open will open the directory in explorer.exe
-cscopy will copy the cloud service project directory into a directory called ".parent"; Ignore this directory for now

Follow the instructions and select which projects are Common, Workerroles and webroles.

Keep in mind when re-coding: You are abandoning the Cloud Service App paradigm, anything that
requires PaaSs will not work in the IaaS paradigm

### Running final checks

You will then need to open each project and make sure it can run on its own.
Once you have made sure everything runs in Visual Studio, run a final check:

```prescript.cmd -check```

This check will confirm that your connections strings are not using development storage
and also make sure everything compiles properly.

If you would like to ignore the database configuration string check, you can run

```prescript.cmd -check -ignoredb```

This will skip the connection strings check and check project compilation

If there are issues compiling, they will be logged under `__save\vms\<name_of_role>\.errors`

If your project compiles in Visual Studio and not with this script, you can skip this step by adding `.confirm`
to the same directory and deleting `.errors`

### Preparing your projects for main.cmd

If your check passes (or you are pleased with your current project), you will need to run

```prescript.cmd -updatesln```

This will then update the .sln file to include the directory ".\.parent\". Once you run this command,
opening the project again in Visual Studio may mess it up.

### Starting over

If you would like to start over, you can either delete the __save directory or run

```prescript.cmd -clear```

This will reset the project back to 0, and therefore you will need to go through this guide again.


## Migrating Azure CSA to VM Operations

Once you have completed prescript steps, you can run:

```main.cmd -mode vm -VMAdmin "Norton" -VMPassword "$3cur3P@$$w0rd"```

And it will deploy a VM for each role you specified

### Provide Credentials
Provide credentials you use to log into http://portal.azure.com

### Invoke main.py
This script will package the script to individual directoriess with GUIDs as the directory
name. Inside will contain compiled versions of each project defined in `.\__save\vms\`.

Once this step is complete, a file called `.confirm_a` will be created. Delete this
file and directories with guid as their names if you want to re-run the packaging script again.

### Get/Build Resource Group

### Get/Build Storage + Container
Will also create keys to access storage/container

### Upload packages to storage/container
All directories under GUID names will have a zip called `zip\_AB\_package.zip`.
This file will be uploaded to the container to be deployed onto a VM

### Save VM variables
A csv will be creteated containing details about the VM to be created.

### Generate Azure Resource Management Templates (arm templates)
For each project guid under `.\__save\`, define a template for deployment
The files `armtemplate.json` and `armtemplate.params.json` are then created.

### Upload webrole script and workerrole script
Custom scripts saved under `.\psscripts\` called `webrole.ps1` and `workerrole.ps1` are then saved
to the cloud for the VMs to use.

### Deploy VM
This is the longest step, and it usually takes about 15 minutes per VM to deploy.

### Run custom extensions
The scripts uploaded earlier will be run (webrole script/workerrole script)

#### WebRole
This script just install IIS components, downloads the zip package onto the VM
and points IIS to serve out of it.

#### WorkerRole
This script downloads the workerrole package and sets the bootstrapper to run upon
boot.

### Checkout each of the VMs
To ensure that the script worked correctly, you will need to login to
http://portal.azure.com and RDC into each VM to make sure it is configured properly.


### Run get\_golden\_image.cmd
While you're connected to the remote, run C:\sysprepme.cmd to run sysprep and shut the vm down. Once you have
done that, you can run the same script with a vmss flag.

## Migrating Azure VM to VMss Operations
Once you have set up your VMs and sysprepped them, you can now run

```main.cmd -mode vmss```

This will create VMSS out of your VMs.

### Set ACL to public
When the script asks for your password, you will need to go to azure and set all container
access policies to public.

### Enter new password
Set your password for each VMSS

# Common Issues
## `No connection could be made ... 127.0.0.1:*`
If you run into this issue, it means your db connection strings are using `useDevelopmentStorage=true`.
Correct them and try re-uploading the packages.

![Issue](http://imgur.com/4Ksrpk7.png)


# Suggestions? Questions?
You can reach me at v-nopeng@microsoft.com or npengra317@gmail.com.