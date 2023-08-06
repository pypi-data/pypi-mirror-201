from prettytable import PrettyTable

from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.core.request_service import Request
from e2e_cli.core.alias_service import get_user_cred
from e2e_cli.core.helper_service import Checks
from e2e_cli.core.constants import BASE_URL


class autoscaling_Crud:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        if(get_user_cred(kwargs['alias'])):
            self.API_key=get_user_cred(kwargs['alias'])[1]
            self.Auth_Token=get_user_cred(kwargs['alias'])[0]
            self.possible=True
        else:
            self.possible=False
        

    def create_autoscaling(self):
        Py_version_manager.py_print("Currently not integrated")
        # my_payload= {}  
        # autoscaling_name=Py_version_manager.py_input("input name of your new autoscaling : ")
        # while(Checks.autoscaling_name_validity(autoscaling_name)):
        #         autoscaling_name=Py_version_manager.py_input("Only following chars are supported: lowercase letters (a-z) or numbers(0-9)  Re-enter : ")

        # API_key=self.API_key
        # Auth_Token=self.Auth_Token
        # url =  BASE_URL+"myaccount/api/v1/storage/autoscalings/"+ autoscaling_name +"/?apikey="+API_key+"&location=Delhi"
        # req="POST"
        # status=Request(url, Auth_Token, my_payload, req).response.json()
               
        # if Checks.status_result(status, req):
        #     try:
        #         x = PrettyTable()
        #         x.field_names = ["ID", "Name", "Created at"]
        #         x.add_row([status['data']['id'], status['data']['name'], status['data']['created_at']])
        #         Py_version_manager.py_print(x)
        #     except Exception as e:
        #               Checks.show_json(status, e)
        #               return
                  
        # Checks.show_json(status)    


    def delete_autoscaling(self):
        my_payload={}
        autoscaling_id=Checks.take_input(self.kwargs["inputs"], "autoscaling_id")
        while(not Checks.is_int(autoscaling_id)):
                autoscaling_id=Py_version_manager.py_input("Only integers allowed ")
        
        API_key=self.API_key
        Auth_Token=self.Auth_Token
        url =  BASE_URL+"myaccount/api/v1/scaler/scalegroups/"+ autoscaling_id +"?apikey="+API_key
        req="DELETE"
        status=Request(url, Auth_Token, my_payload, req).response.json()

        if Checks.status_result(status,req):
                        Py_version_manager.py_print("autoscaling Successfully deleted")
                        Py_version_manager.py_print("use following command -> e2e_cli <alias> autoscaling list to check if autoscaling has been deleted")
        
        if('json' in self.kwargs["inputs"]):
            Checks.show_json(status)


    def list_autoscaling(self):
        my_payload={}
        API_key= self.API_key  
        Auth_Token= self.Auth_Token 
        url =  BASE_URL+"myaccount/api/v1/scaler/scalegroups?apikey="+ API_key+"&location=Delhi"
        req="GET"
        status=Request(url, Auth_Token, my_payload, req).response.json()
        
        if Checks.status_result(status, req):
                Py_version_manager.py_print("Your autoscalings : ")
                try:
                    list=status['data']
                    i=1
                    x = PrettyTable()
                    x.field_names = ["index", "ID", "Policy", "Name", "Max_nodes", "Min_nodes"]
                    for element in list:
                        x.add_row([i, element['id'], element['policy'], element['name'], element['max_nodes'], element["min_nodes"]])
                        i = i+1
                    Py_version_manager.py_print(x)
                except Exception as e:
                      Py_version_manager.py_print("Errors : ", e)
                        
        if('json' in self.kwargs["inputs"]):
                    Checks.show_json(status)
    

