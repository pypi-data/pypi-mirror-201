from prettytable import PrettyTable
import json

from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.core.request_service import Request
from e2e_cli.core.alias_service import get_user_cred
from e2e_cli.core.helper_service import Checks
from e2e_cli.core.constants import BASE_URL


class volumes_Crud:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        if(get_user_cred(kwargs['alias'])):
            self.API_key=get_user_cred(kwargs['alias'])[1]
            self.Auth_Token=get_user_cred(kwargs['alias'])[0]
            self.possible=True
        else:
            self.possible=False
        

    def create_volumes(self):
        Py_version_manager.py_print("Creating")
        iops_list=dict({
                "250" : "5000", "500" : "10000", "1000" : "20000",  "2000" : "40000",  "4000" : "80000", "8000" : "120000", "16000" : "120000"
        })
        Py_version_manager.py_print("Enter size, multiple of 250GB only")
        size=Checks.take_input(self.kwargs["inputs"], "size")
        my_payload= json.dumps({
            "name": Checks.take_input(self.kwargs["inputs"], "name"),
            "size": size,
            "iops": iops_list[size]
        })
        API_key=self.API_key
        Auth_Token=self.Auth_Token
        url =  BASE_URL+"myaccount/api/v1/block_storage/?apikey="+API_key+"&location=Delhi"
        req="POST"
        status=Request(url, Auth_Token, my_payload, req).response.json()
               
        if Checks.status_result(status, req):
            try:
                x = PrettyTable()
                x.field_names = ["block_storage_id", "name"]
                x.add_row([status['data']['block_storage_id'], status['data']['image_name']])
                Py_version_manager.py_print(x)
            except Exception as e:
                      Checks.show_json(status, e)
                      return
                  
        if('json' in self.kwargs["inputs"]):
            Checks.show_json(status)     


    def delete_volumes(self):
        my_payload={}
        blockstorage_id=Checks.take_input(self.kwargs["inputs"], "blockstorage_id")
        API_key=self.API_key
        Auth_Token=self.Auth_Token
        url =  BASE_URL+"myaccount/api/v1/block_storage/"+blockstorage_id+"/?apikey="+API_key+"&location=Delhi"
        req="DELETE"
        status=Request(url, Auth_Token, my_payload, req).response.json()

        if Checks.status_result(status,req):
                        Py_version_manager.py_print("volume Successfully deleted")
                        Py_version_manager.py_print("use following command -> e2e_cli <alias> volumes list to check if volumes has been deleted")
        
        Checks.show_json(status)


    def list_volumes(self):
        my_payload={}
        API_key= self.API_key  
        Auth_Token= self.Auth_Token 
        url =  BASE_URL+"myaccount/api/v1/block_storage/?apikey="+ API_key+"&location=Delhi"
        req="GET"
        status=Request(url, Auth_Token, my_payload, req).response.json()
        
        if Checks.status_result(status, req):
                Py_version_manager.py_print("Your volumess : ")
                try:
                    list=status['data']
                    i=1
                    x = PrettyTable()
                    x.field_names = ["index", "name", "block_id", "status"]
                    for element in list:
                        x.add_row([i, element['name'], element['block_id'], element["status"]])
                        i = i+1
                    Py_version_manager.py_print(x)
                except Exception as e:
                    Py_version_manager.py_print("Errors : ", e)

        if('json' in self.kwargs["inputs"]):
            Checks.show_json(status) 
    



