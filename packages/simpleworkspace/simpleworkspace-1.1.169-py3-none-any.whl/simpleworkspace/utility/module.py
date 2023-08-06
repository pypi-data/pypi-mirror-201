import sys as _sys

def RequireModules(modules: list[str]) -> bool:
    '''
    Checks if python modules are installed, otherwise tries to install them
    '''
    import importlib
    import subprocess
    import pkg_resources
    
    required = modules
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = required - installed
    if missing:
        print("Please wait a moment, application is missing some modules. These will be installed automatically...")
        python = _sys.executable
        for i in missing:
            try:
                subprocess.check_call([python, "-m", "pip", "install", i])
            except Exception as e:
                pass
    importlib.reload(pkg_resources)
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = required - installed
    if missing:
        print("Not all required modules could automatically be installed!")
        print("Please install the modules below manually:")
        for i in missing:
            print("    -" + i)
        return False
    return True

def ImportModuleDynamically(moduleName, path):
    '''
    @param moduleName: freely name the module to import
    @param path: full path to the python module
    '''
    import importlib.util
    import os

    spec = importlib.util.spec_from_file_location(moduleName, path)
    mod = importlib.util.module_from_spec(spec)
    _sys.modules[moduleName] = mod
    _sys.path.append(os.path.dirname(os.path.abspath(path)))
    spec.loader.exec_module(mod)
    return mod