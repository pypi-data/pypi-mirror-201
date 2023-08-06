from importlib import import_module
from collections import defaultdict

def parse_model_id(model_id):
    return model_id.lower().replace("-","_")

def get_model_function(model_id, module_name, function_name):
    model_id = parse_model_id(model_id)
    try:
        module = import_module("submodules.MOAP_core.moap.{}.{}".format(model_id, module_name))
    except ModuleNotFoundError:
        raise "Modules not found for {}.".format(model_id)
    try:
        func = module.__getattribute__(function_name)
    except AttributeError:
        raise "Function {} not found for model_id {}.".format(function_name, model_id)
    return func

