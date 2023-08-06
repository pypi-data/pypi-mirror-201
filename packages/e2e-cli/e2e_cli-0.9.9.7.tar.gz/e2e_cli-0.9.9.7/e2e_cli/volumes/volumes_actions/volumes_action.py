from prettytable import PrettyTable
import json

from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.core.request_service import Request
from e2e_cli.core.alias_service import get_user_cred
from e2e_cli.core.helper_service import Checks
from e2e_cli.core.constants import BASE_URL


class volumesActions:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        if(get_user_cred(kwargs['alias'])):
            self.API_key=get_user_cred(kwargs['alias'])[1]
            self.Auth_Token=get_user_cred(kwargs['alias'])[0]
            self.possible=True
        else:
            self.possible=False


    def attach_volume(self):
        my_payload= json.dumps({
            "vm_id": Py_version_manager.py_input("enter vm id of node you want to attach volume ")
            })
        blockstorage_id=Py_version_manager.py_input("input blockstorage_id of the volumes you want to delete : ")
        API_key=self.API_key
        Auth_Token=self.Auth_Token
        url =  BASE_URL+"myaccount/api/v1/block_storage/"+blockstorage_id+"/vm/attach/?apikey="+API_key+"&location=Delhi"
        req="POST"
        status=Request(url, Auth_Token, my_payload, req).response.text

        Checks.show_json(status)

    def attach_volume(self):
        my_payload= json.dumps({
            "vm_id": Py_version_manager.py_input("enter vm id of node you want to attach volume ")
            })
        blockstorage_id=Py_version_manager.py_input("input blockstorage_id of the volumes you want to delete : ")
        API_key=self.API_key
        Auth_Token=self.Auth_Token
        url =  BASE_URL+"myaccount/api/v1/block_storage/"+blockstorage_id+"/vm/detach/?apikey="+API_key+"&location=Delhi"
        req="POST"
        status=Request(url, Auth_Token, my_payload, req).response.text

        Checks.show_json(status)

    
    