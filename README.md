# Cloud2VMSS

The objective of this project is to specify a Solution directory and build Virtual Machine Scalable Sets out of it.

The point of this is to convert the existing [Paas](https://en.wikipedia.org/wiki/Platform_as_a_service) to a [Iaas](https://en.wikipedia.org/wiki/Cloud_computing#Infrastructure_as_a_service_.28IaaS.29) so developers can take advantage of
all the new technologies that come out that they wouldn't normally get using the Cloud App Service ([Paas](https://en.wikipedia.org/wiki/Platform_as_a_service))

## How to use this project

### Using the Prescript to prime the project
You will first need to use the pre-script to split the cloud app into seperate projects:

```prescript.cmd "C:\Path\To\Project" -open -cscopy```

Follow the instructions and select which projects are Common, Workerroles and webroles.

You will then need to open each project and make sure it can run on its own.
Once you have made sure everything runs in Visual Studio, run a final check:

```prescript.cmd -check```

This check will confirm that your connections strings are not using development storage
and also make sure everything compiles properly.

If there are issues compiling, they will be logged under `__save\vms\<name_of_role>\.errors`

If your project compiles in Visual Studio and not with this script, you can skip this step by adding `.confirm`
to the same directory and deleting `.errors`

If your check passes, you will need to run

```prescript.cmd -updatesln```

This will then update the .sln file to include the directory ".parent". Once you run this command,
opening the project again in Visual Studio may mess it up.

### Migrating Azure CSA to VMSS

Once you have complited prescript steps, you can run:

```main.cmd -VMAdmin "Norton" -VMPassword "$3cur3P@$$w0rd"```

And it will deploy a VM for each role you specified

# Suggestions? Questions?
You can reach me v-nopeng@microsoft.com or npengra317@gmail.com.