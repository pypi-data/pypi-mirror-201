import json
import os
import platform

from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.core.constants import RESERVES


# def option_check(alias):
#     if(alias=="default"):
#             return get_user_cred(alias)[0]
#     else:
#           return alias


class AliasServices:
    def __init__(self, alias):
        self.alias = alias

    def get_api_credentials(self):
        file= os.path.expanduser("~") + '/.E2E_CLI/config.json'
        file_reference = open(file, "r")
        config_file_object = json.loads(file_reference.read())
        if self.alias in config_file_object:
            if(self.alias=="default"):
                default_alias=config_file_object["default"]['api_key']
                return {"api_credentials": config_file_object[default_alias],
                        "message": "Valid alias"}
            else:
                return {"api_credentials": config_file_object[self.alias],
                        "message": "Valid alias"}
        else:
            return {"message": "Invalid alias provided"}

def system_file():
    if platform.system() == "Windows":  
                return os.path.expanduser("~") + '\.E2E_CLI\config.json'
    elif platform.system() == "Linux" or platform.system() == "Darwin":  
                return os.path.expanduser("~") + '/.E2E_CLI/config.json'


def get_user_cred(name, x=0):
    
    file= system_file()

    # try :
    # Opening JSON file
    f = open(file)
    
    # returns JSON object as a dictionary
    data = json.load(f)

    if(name=="all" and x==1):
                try:
                    Py_version_manager.py_print("default --> ", data["default"])
                except:
                    Py_version_manager.py_print("default --> ", "Not set")
                return data.keys()
    
    # Closing file
    f.close()


    if(name in data):
        if(name=="default"):
            return get_user_cred(data["default"]['api_key'])
        else:  
            return[ data[name]['api_auth_token'], data[name]['api_key'] ]
    elif x==2:
        return None
    else:
        Py_version_manager.py_print("Warning : The given alias/credential doesn't exist")
        return None
