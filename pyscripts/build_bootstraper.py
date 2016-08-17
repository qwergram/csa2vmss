# This script builds a bootstrapper for the worker role
import io
import json

def load_appconfig(location):
    print("Load app.config")
    with io.open(location) as context:
        return context.read()

def load_assemblyinfo(location):
    with io.open(location) as context:
        return context.read()

def load_csproj(location):
    with io.open(location) as context:
        return context.read()
    

def load_bootstrapper(location, workername, classname):
    with io.open(location) as context:
        bootstrap = context.read()
    bootstrap = bootstrap.replace("{$WORKERNAME!}", workername).replace("{$CLASSNAME!}", classname)
    return bootstrap

def main(data={}):
    print(json.dumps(data, indent=2))
    # global APPCONFIG, ASSEMBLIES, CSPROJ, BOOTSTRAP
    # print("Building bootstrapper")
    # APPCONFIG = load_appconfig()
    # ASSEMBLIES = load_assemblyinfo()
    # CSPROJ = load_csproj()
    # BOOTSTRAP = load_bootstrapper()

if __name__ == "__main__":
    main()