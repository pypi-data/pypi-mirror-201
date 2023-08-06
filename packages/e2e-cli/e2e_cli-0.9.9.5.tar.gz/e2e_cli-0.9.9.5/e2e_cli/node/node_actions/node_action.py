from prettytable import PrettyTable
import json

from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.core.request_service import Request
from e2e_cli.core.alias_service import get_user_cred
from e2e_cli.core.helper_service import Checks
from e2e_cli.core.constants import BASE_URL


class nodeActions:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        if(get_user_cred(kwargs['alias'])):
            self.API_key=get_user_cred(kwargs['alias'])[1]
            self.Auth_Token=get_user_cred(kwargs['alias'])[0]
            self.possible=True
        else:
            self.possible=False


    def action_table(self, status, req):
        if Checks.status_result(status, req):
                try:
                    x = PrettyTable()
                    x.field_names = ["Action_type", "Status", "Action ID"]
                    x.add_row([status['data']['action_type'],
                            status['data']['status'], status['data']['id']])
                    Py_version_manager.py_print(x)
                except Exception as e:
                        Py_version_manager.py_print("Errors while reading json ", str(e))
                
        if('json' in self.kwargs["inputs"]):
            Checks.show_json(status)


    def node_monitoring(self):
        my_payload= {}
        node_id = Checks.take_input(self.kwargs["inputs"], "node_id")
        while(not Checks.is_int(node_id)):
              node_id = Py_version_manager.py_input("please enter node id (integer only) ")
        
        API_key=self.API_key
        Auth_Token=self.Auth_Token
        url =  BASE_URL+"myaccount/api/v1/nodes/"+ node_id +"/monitor/server-health/?&apikey="+API_key
        req="GET"
        status=Request(url, Auth_Token, my_payload, req).response.json()

        self.action_table(status, req) 


    
    def enable_recovery(self):
        my_payload= json.dumps({
                       "type": "enable_recovery_mode"
                }) 
        node_id = Checks.take_input(self.kwargs["inputs"], "node_id")
        while(not Checks.is_int(node_id)):
              node_id = Py_version_manager.py_input("please enter node id (integer only) ")
        
        API_key=self.API_key
        Auth_Token=self.Auth_Token
        url =  BASE_URL+"myaccount/api/v1/nodes/"+ node_id +"/actions/?apikey="+API_key+"&location=Delhi"
        req="POST"
        status=Request(url, Auth_Token, my_payload, req).response.json()
        
        self.action_table(status, req)                 


    def disable_recovery(self):
        my_payload= json.dumps({
                      "type": "disable_recovery_mode"
               })  
        node_id = Checks.take_input(self.kwargs["inputs"], "node_id")
        while(not Checks.is_int(node_id)):
              node_id = Py_version_manager.py_input("please enter node id (integer only) ")
        
        API_key=self.API_key
        Auth_Token=self.Auth_Token
        url =  BASE_URL+"myaccount/api/v1/nodes/"+ node_id +"/actions/?apikey="+API_key+"&location=Delhi"
        req="POST"
        status=Request(url, Auth_Token, my_payload, req).response.json()
        
        self.action_table(status, req)
               


    def reinstall(self):
        my_payload= json.dumps({
                        "type": "reinstall"
                      })  
        node_id = Checks.take_input(self.kwargs["inputs"], "node_id")
        while(not Checks.is_int(node_id)):
              node_id = Py_version_manager.py_input("please enter node id (integer only) ")
        
        API_key=self.API_key
        Auth_Token=self.Auth_Token
        url =  BASE_URL+"myaccount/api/v1/nodes/"+ node_id +"/actions/?apikey="+API_key+"&location=Delhi"
        req="POST"
        status=Request(url, Auth_Token, my_payload, req).response.json()
        
        self.action_table(status, req)    
         


    def reboot(self):
        my_payload= json.dumps({
                           "type": "reboot"
                        })  
        node_id = Checks.take_input(self.kwargs["inputs"], "node_id")
        while(not Checks.is_int(node_id)):
              node_id = Py_version_manager.py_input("please enter node id (integer only) ")
        
        API_key=self.API_key
        Auth_Token=self.Auth_Token
        url =  BASE_URL+"myaccount/api/v1/nodes/"+ node_id +"/actions/?apikey="+API_key+"&location=Delhi"
        req="POST"
        status=Request(url, Auth_Token, my_payload, req).response.json()
        
        self.action_table(status, req)                  



    def power_on(self):
        my_payload= json.dumps({
                        "type": "power_on"
                  }) 
        node_id = Checks.take_input(self.kwargs["inputs"], "node_id")
        while(not Checks.is_int(node_id)):
              node_id = Py_version_manager.py_input("please enter node id (integer only) ")
        
        API_key=self.API_key
        Auth_Token=self.Auth_Token
        url =  BASE_URL+"myaccount/api/v1/nodes/"+ node_id +"/actions/?apikey="+API_key+"&location=Delhi"
        req="POST"
        status=Request(url, Auth_Token, my_payload, req).response.json()
        
        self.action_table(status, req)              
        


    def power_off(self):
        my_payload= json.dumps({
                         "type": "power_off"
                 })  
        node_id = Checks.take_input(self.kwargs["inputs"], "node_id")
        while(not Checks.is_int(node_id)):
              node_id = Py_version_manager.py_input("please enter node id (integer only) ")
        
        API_key=self.API_key
        Auth_Token=self.Auth_Token
        url =  BASE_URL+"myaccount/api/v1/nodes/"+ node_id +"/actions/?apikey="+API_key+"&location=Delhi"
        req="POST"
        status=Request(url, Auth_Token, my_payload, req).response.json()
        
        self.action_table(status, req)             
    


    def rename_node(self):
        node_id = Checks.take_input(self.kwargs["inputs"], "node_id")
        while(not Checks.is_int(node_id)):
              node_id = Py_version_manager.py_input("please enter node id (integer only) ")
        new_name=Py_version_manager.py_input("please enter new name for the node : ")
        my_payload= json.dumps({
                       "name": new_name,
                       "type": "rename"
                  })  
        
        API_key=self.API_key
        Auth_Token=self.Auth_Token
        url =  BASE_URL+"myaccount/api/v1/nodes/"+ node_id +"/actions/?apikey="+API_key+"&location=Delhi"
        req="POST"
        status=Request(url, Auth_Token, my_payload, req).response.json()
        
        self.action_table(status, req)
               
        

    def unlock_vm(self):
        my_payload= json.dumps({
                        "type": "unlock_vm"
                 })  
        node_id = Checks.take_input(self.kwargs["inputs"], "node_id")
        while(not Checks.is_int(node_id)):
              node_id = Py_version_manager.py_input("please enter node id (integer only) ")
        
        API_key=self.API_key
        Auth_Token=self.Auth_Token
        url =  BASE_URL+"myaccount/api/v1/nodes/"+ node_id +"/actions/?apikey="+API_key+"&location=Delhi"
        req="POST"
        status=Request(url, Auth_Token, my_payload, req).response.json()
        
        self.action_table(status, req)
               
    

    def lock_vm(self):
        my_payload= json.dumps({
                        "type": "lock_vm"
                 })  
        node_id = Checks.take_input(self.kwargs["inputs"], "node_id")
        while(not Checks.is_int(node_id)):
              node_id = Py_version_manager.py_input("please enter node id (integer only) ")
        
        API_key=self.API_key
        Auth_Token=self.Auth_Token
        url =  BASE_URL+"myaccount/api/v1/nodes/"+ node_id +"/actions/?apikey="+API_key+"&location=Delhi"
        req="POST"
        status=Request(url, Auth_Token, my_payload, req).response.json()
        
        self.action_table(status, req)
               
        
        
    