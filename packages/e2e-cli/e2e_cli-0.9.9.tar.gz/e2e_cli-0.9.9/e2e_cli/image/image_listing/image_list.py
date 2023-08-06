from prettytable import PrettyTable
import json

from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.core.request_service import Request
from e2e_cli.core.alias_service import get_user_cred
from e2e_cli.core.helper_service import Checks
from e2e_cli.core.constants import BASE_URL


class ImageListing:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        if(get_user_cred(kwargs['alias'])):
            self.API_key=get_user_cred(kwargs['alias'])[1]
            self.Auth_Token=get_user_cred(kwargs['alias'])[0]
            self.possible=True
        else:
            self.possible=False


    def image_type(self):
        my_payload= {}    
        API_key=self.API_key
        Auth_Token=self.Auth_Token
        url =  BASE_URL+"myaccount/api/v1/images/?apikey="+API_key+"&image_type=private"
        req="GET"
        status=Request(url, Auth_Token, my_payload, req).response.json()

        Py_version_manager.py_print(status)            
            
        query=dict()
        
        cpu=Py_version_manager.py_input("number of CPU ")
        ram=Py_version_manager.py_input("capacity of RAM in GB ")
        series=Py_version_manager.py_input("input the Series ")
        OS=Py_version_manager.py_input("input the OS ")
        Version=Py_version_manager.py_input("input the OS Version ")


    
        
        
    