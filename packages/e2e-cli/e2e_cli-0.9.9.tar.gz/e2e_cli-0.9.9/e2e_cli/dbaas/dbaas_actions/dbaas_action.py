from prettytable import PrettyTable
import json

from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.core.request_service import Request
from e2e_cli.core.alias_service import get_user_cred
from e2e_cli.core.helper_service import Checks
from e2e_cli.core.constants import BASE_URL


class DBaasAction:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        if(get_user_cred(kwargs['alias'])):
            self.API_key=get_user_cred(kwargs['alias'])[1]
            self.Auth_Token=get_user_cred(kwargs['alias'])[0]
            self.possible=True
        else:
            self.possible=False


    def take_snapshot(self):
        dbaas_id =Checks.take_input(self.kwargs["inputs"], "dbaas_id")
        while(not Checks.is_int(dbaas_id )):
                dbaas_id =Py_version_manager.py_input("Only integers : ")
        my_payload= json.dumps({
                "name": "sanap3"
                })
        API_key=self.API_key
        Auth_Token=self.Auth_Token
        url =  BASE_URL+"myaccount/api/v1/rds/cluster/"+ dbaas_id +"/snapshot?apikey="+API_key
        req="POST"
        status=Request(url, Auth_Token, my_payload, req).response.json()

        Checks.status_result(status)
        Checks.show_json(status)


    def reset_password(self):
        dbaas_id =Checks.take_input(self.kwargs["inputs"], "dbaas_id")
        while(not Checks.is_int(dbaas_id )):
                dbaas_id =Py_version_manager.py_input("Only integers : ")
        my_payload= json.dumps({
                 "password": Checks.take_input(self.kwargs["inputs"], "new_password"),
                 "username": Checks.take_input(self.kwargs["inputs"], "username")
                })
        API_key=self.API_key
        Auth_Token=self.Auth_Token
        url =  BASE_URL+"myaccount/api/v1/rds/cluster/"+dbaas_id+"/reset-password/?apikey="+API_key
        req="POST"
        status=Request(url, Auth_Token, my_payload, req).response.json()

        Checks.status_result(status)
        Checks.show_json(status)


    def stop_db(self):
        dbaas_id =Checks.take_input(self.kwargs["inputs"], "dbaas_id")
        while(not Checks.is_int(dbaas_id )):
                dbaas_id =Py_version_manager.py_input("Only integers : ")
        my_payload= {}
        API_key=self.API_key
        Auth_Token=self.Auth_Token
        url =  BASE_URL+"myaccount/api/v1/rds/cluster/"+dbaas_id+"/shutdown?apikey="+API_key
        req="POST"
        status=Request(url, Auth_Token, my_payload, req).response.json()

        Checks.status_result(status)
        Checks.show_json(status)


    def start_db(self):
        dbaas_id =Checks.take_input(self.kwargs["inputs"], "dbaas_id")
        while(not Checks.is_int(dbaas_id )):
                dbaas_id =Py_version_manager.py_input("Only integers : ")
        my_payload= {}
        API_key=self.API_key
        Auth_Token=self.Auth_Token
        url =  BASE_URL+"myaccount/api/v1/rds/cluster/"+dbaas_id+"/resume?apikey="+API_key
        req="POST"
        status=Request(url, Auth_Token, my_payload, req).response.json()

        Checks.status_result(status)
        Checks.show_json(status)

    
    def restart_db(self):
        dbaas_id =Checks.take_input(self.kwargs["inputs"], "dbaas_id")
        while(not Checks.is_int(dbaas_id )):
                dbaas_id =Py_version_manager.py_input("Only integers : ")
        my_payload= {}
        API_key=self.API_key
        Auth_Token=self.Auth_Token
        url =  BASE_URL+"myaccount/api/v1/rds/cluster/"+dbaas_id+"/restart?apikey="+API_key
        req="POST"
        status=Request(url, Auth_Token, my_payload, req).response.json()

        Checks.status_result(status)
        Checks.show_json(status)


    def add_parameter_group(self):
        dbaas_id =Checks.take_input(self.kwargs["inputs"], "dbaas_id")
        while(not Checks.is_int(dbaas_id )):
                dbaas_id =Py_version_manager.py_input("Only integers : ")
        parameter_group_id =Checks.take_input(self.kwargs["inputs"], "parameter_group_id")
        while(not Checks.is_int(parameter_group_id )):
                parameter_group_id =Py_version_manager.py_input("Only integers : ")
        my_payload= {}
        API_key=self.API_key
        Auth_Token=self.Auth_Token
        url =  BASE_URL+"myaccount/api/v1/rds/cluster/"+dbaas_id+"/parameter-group/"+parameter_group_id+"/add?apikey="+API_key
        req="POST"
        status=Request(url, Auth_Token, my_payload, req).response.json()

        Checks.status_result(status)
        Checks.show_json(status)
    

    def remove_parameter_group(self):
        dbaas_id =Checks.take_input(self.kwargs["inputs"], "dbaas_id")
        while(not Checks.is_int(dbaas_id )):
                dbaas_id =Py_version_manager.py_input("Only integers : ")
        parameter_group_id =Checks.take_input(self.kwargs["inputs"], "parameter_group_id")
        while(not Checks.is_int(parameter_group_id )):
                parameter_group_id =Py_version_manager.py_input("Only integers : ")
        my_payload= {}
        API_key=self.API_key
        Auth_Token=self.Auth_Token
        url =  BASE_URL+"myaccount/api/v1/rds/cluster/"+dbaas_id+"/parameter-group/"+parameter_group_id+"/detach?apikey="+API_key
        req="POST"
        status=Request(url, Auth_Token, my_payload, req).response.json()

        Checks.status_result(status)
        Checks.show_json(status)
    

    def add_vpc(self):
        dbaas_id =Checks.take_input(self.kwargs["inputs"], "dbaas_id")
        while(not Checks.is_int(dbaas_id )):
                dbaas_id =Py_version_manager.py_input("Only integers : ")
        my_payload= json.dumps({
                   "action": "attach",
                   "network_id": Checks.take_input(self.kwargs["inputs"], "network_id")
                     })
        API_key=self.API_key
        Auth_Token=self.Auth_Token
        url =  BASE_URL+"myaccount/api/v1/rds/cluster/"+dbaas_id+"//vpc-attach/?apikey="+API_key
        req="POST"
        status=Request(url, Auth_Token, my_payload, req).response.json()

        Checks.status_result(status)
        Checks.show_json(status)


    def remove_vpc(self):
        dbaas_id =Checks.take_input(self.kwargs["inputs"], "dbaas_id")
        while(not Checks.is_int(dbaas_id )):
                dbaas_id =Py_version_manager.py_input("Only integers : ")
        my_payload= json.dumps({
                   "action": "detach",
                   "network_id": Checks.take_input(self.kwargs["inputs"], "network_id")
                     })
        API_key=self.API_key
        Auth_Token=self.Auth_Token
        url =  BASE_URL+"myaccount/api/v1/rds/cluster/"+dbaas_id+"/vpc-detach/?apikey="+API_key
        req="POST"
        status=Request(url, Auth_Token, my_payload, req).response.json()

        Checks.status_result(status)
        Checks.show_json(status)


    def enable_backup(self):
        dbaas_id =Checks.take_input(self.kwargs["inputs"], "dbaas_id")
        while(not Checks.is_int(dbaas_id )):
                dbaas_id =Py_version_manager.py_input("Only integers : ")
        my_payload= json.dumps({
                 "access_key": Checks.take_input(self.kwargs["inputs"], "access_key"),
                 "bucket_location": Checks.take_input(self.kwargs["inputs"], "bucket_location"),
                 "secret_key": Checks.take_input(self.kwargs["inputs"], "secret_key")
                    })
        API_key=self.API_key
        Auth_Token=self.Auth_Token
        url =  BASE_URL+"myaccount/api/v1/rds/cluster/"+dbaas_id+"/enable-backup?apikey="+API_key
        req="POST"
        status=Request(url, Auth_Token, my_payload, req).response.json()

        Checks.status_result(status)
        Checks.show_json(status)


    def disable_backup(self):
        dbaas_id =Checks.take_input(self.kwargs["inputs"], "dbaas_id")
        while(not Checks.is_int(dbaas_id )):
                dbaas_id =Py_version_manager.py_input("Only integers : ")
        my_payload= {}
        API_key=self.API_key
        Auth_Token=self.Auth_Token
        url =  BASE_URL+"myaccount/api/v1/rds/cluster/"+dbaas_id+"/disable-backup?apikey="+API_key
        req="POST"
        status=Request(url, Auth_Token, my_payload, req).response.json()

        Checks.status_result(status)
        Checks.show_json(status)