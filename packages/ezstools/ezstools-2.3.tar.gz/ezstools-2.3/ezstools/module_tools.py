import importlib

def new_module(mod_name):
    spec = importlib.machinery.ModuleSpec(mod_name,None)
    return importlib.util.module_from_spec(spec)

def create_module(mod_name, **atributes):

    mod = new_module(mod_name)
    for name, value in atributes.items():
        setattr(mod, name, value)

    return mod
