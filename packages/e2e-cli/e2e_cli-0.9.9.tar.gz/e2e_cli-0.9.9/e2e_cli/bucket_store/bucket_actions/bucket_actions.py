from prettytable import PrettyTable
import json

from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.core.request_service import Request
from e2e_cli.core.alias_service import get_user_cred
from e2e_cli.core.helper_service import Checks
from e2e_cli.core.constants import BASE_URL


class BucketActions:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        if(get_user_cred(kwargs['alias'])):
            self.API_key=get_user_cred(kwargs['alias'])[1]
            self.Auth_Token=get_user_cred(kwargs['alias'])[0]
            self.possible=True
        else:
            self.possible=False


    def enable_versioning(self):
        bucket_name=Checks.take_input(self.kwargs["inputs"], "bucket_name")
        while(Checks.bucket_name_validity(bucket_name)):
                bucket_name=Py_version_manager.py_input("Only following chars are supported: lowercase letters (a-z) or numbers(0-9)  Re-enter : ")
        my_payload= json.dumps({
                        "bucket_name": bucket_name,
                        "new_versioning_state": "Enabled"
                }) 
        
        API_key=self.API_key
        Auth_Token=self.Auth_Token
        url =  BASE_URL+"myaccount/api/v1/storage/bucket_versioning/"+ bucket_name +"/?apikey="+API_key+"&location=Delhi"
        req="POST"
        status=Request(url, Auth_Token, my_payload, req).response.json()

        Checks.status_result(status)
        Checks.show_json(status)


    def disable_versioning(self):
        bucket_name=Checks.take_input(self.kwargs["inputs"], "bucket_name")
        while(Checks.bucket_name_validity(bucket_name)):
                bucket_name=Py_version_manager.py_input("Only following chars are supported: lowercase letters (a-z) or numbers(0-9)  Re-enter : ")
        my_payload= json.dumps({
                        "bucket_name": bucket_name,
                        "new_versioning_state": "Disabled"
                }) 
        
        API_key=self.API_key
        Auth_Token=self.Auth_Token
        url =  BASE_URL+"myaccount/api/v1/storage/bucket_versioning/"+ bucket_name +"/?apikey="+API_key+"&location=Delhi"
        req="POST"
        status=Request(url, Auth_Token, my_payload, req).response.json()

        Checks.status_result(status)
        Checks.show_json(status)


    def create_key(self):
        key_name=Checks.take_input(self.kwargs["inputs"], "key_name")
        while(Checks.bucket_name_validity(key_name)):
                key_name=Py_version_manager.py_input("Only following chars are supported: lowercase letters (a-z) or numbers(0-9)  Re-enter : ")
        my_payload= json.dumps({
                        "tag": key_name
                }) 
        
        API_key=self.API_key
        Auth_Token=self.Auth_Token
        url =  BASE_URL+"myaccount/api/v1/storage/core/users/?apikey="+API_key+"&location=Delhi"
        req="POST"
        status=Request(url, Auth_Token, my_payload, req).response.json()

        if(Checks.status_result(status)):
              Py_version_manager.py_print("Key Created successfully")

        Checks.show_json(status)
    

    def delete_key(self):
        access_key=Checks.take_input(self.kwargs["inputs"], "access_key")
        my_payload= {} 
        query= dict()
        query['access_key']=access_key
        API_key=self.API_key
        Auth_Token=self.Auth_Token
        url =  BASE_URL+"myaccount/api/v1/storage/core/users/?apikey="+API_key+"&location=Delhi"
        req="DELETE"
        status=Request(url, Auth_Token, my_payload, req, query=query).response.json()

        if(Checks.status_result(status)):
              Py_version_manager.py_print("Key deleted successfully")

        Checks.show_json(status)

    
    def list_key(self):
        my_payload={}
        API_key= self.API_key  
        Auth_Token= self.Auth_Token 
        url =  BASE_URL+"myaccount/api/v1/storage/core/list/users/?apikey="+ API_key+"&location=Delhi"
        req="GET"
        status=Request(url, Auth_Token, my_payload, req).response.json()
        
        if Checks.status_result(status, req):
                Py_version_manager.py_print("Your Keys : ")
                try:
                    list=status['data']
                    i=1
                    x = PrettyTable()
                    x.field_names = ["index", "ID", "Name", "access_key" ]
                    for element in list:
                        x.add_row([i, element['id'], element['tag'], element['access_key']])
                        i = i+1
                    Py_version_manager.py_print(x)
                except Exception as e:
                      Checks.show_json(status, e)
                      return    

        Checks.show_json(status)


    def lock_key(self):
        key_id=Checks.take_input(self.kwargs["inputs"], "key_id")
        while(not Checks.is_int(key_id)):
                key_id=Py_version_manager.py_input("Only integer allowed ")
        my_payload= json.dumps({
                "disabled": True,
                "id": key_id
                }) 
        
        API_key=self.API_key
        Auth_Token=self.Auth_Token
        url =  BASE_URL+"myaccount/api/v1/storage/core/users/?apikey="+API_key+"&location=Delhi"
        req="PUT"
        status=Request(url, Auth_Token, my_payload, req).response.json()
        
        if(Checks.status_result(status)):
              Py_version_manager.py_print("Key locked")

        Checks.show_json(status)

    
    def unlock_key(self):
        key_id=Checks.take_input(self.kwargs["inputs"], "key_id")
        while(not Checks.is_int(key_id)):
                key_id=Py_version_manager.py_input("Only integer allowed ")
        my_payload= json.dumps({
                "disabled": False,
                "id": key_id
                }) 
        
        API_key=self.API_key
        Auth_Token=self.Auth_Token
        url =  BASE_URL+"myaccount/api/v1/storage/core/users/?apikey="+API_key+"&location=Delhi"
        req="PUT"
        status=Request(url, Auth_Token, my_payload, req).response.json()

        if(Checks.status_result(status)):
              Py_version_manager.py_print("Key unlocked")

        Checks.show_json(status)
    

    def add_permission(self):
        bucket_name=Checks.take_input(self.kwargs["inputs"], "bucket_name")
        while(Checks.bucket_name_validity(bucket_name)):
                bucket_name=Py_version_manager.py_input("Only following chars are supported: lowercase letters (a-z) or numbers(0-9)  Re-enter : ")
        my_payload= json.dumps({
            "role_name": "Bucket Admin",
            "users": [
            {
                "access_key": Py_version_manager.py_input("input access key (Alphanumeric): "),
                "disabled": False,
                "email": "",
                "id": Py_version_manager.py_input("enter bucket id "),
                "is_default": False,
                "my_account_id": None,
                "secret_key": None,
                "tag": Py_version_manager.py_input("name "),
                "user_name": Py_version_manager.py_input("username ")
            }
            ]
            })
        query= dict()
        query['bucket_name']=bucket_name
        API_key=self.API_key
        Auth_Token=self.Auth_Token
        url =  BASE_URL+"myaccount/api/v1/storage/bucket_perms/?apikey="+API_key+"&location=Delhi"
        req="PUT"
        status=Request(url, Auth_Token, my_payload, req, query=query).response.json()

        # if(Checks.status_result(status)):
        #       Py_version_manager.py_print("Key deleted successfully")
        Checks.status_result(status)
        Checks.show_json(status)


    def remove_permission(self):
        access_key=Checks.take_input(self.kwargs["inputs"], "access_key")
        my_payload= {} 
        query= dict()
        query['access_key']=access_key
        API_key=self.API_key
        Auth_Token=self.Auth_Token
        url =  BASE_URL+"myaccount/api/v1/storage/core/users/?apikey="+API_key+"&location=Delhi"
        req="DELETE"
        status=Request(url, Auth_Token, my_payload, req, query=query).response.json()

        if(Checks.status_result(status)):
              Py_version_manager.py_print("Key deleted successfully")

        Checks.status_result(status)
        Checks.show_json(status)