from prettytable import PrettyTable

from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.core.request_service import Request
from e2e_cli.core.alias_service import get_user_cred
from e2e_cli.core.helper_service import Checks
from e2e_cli.core.constants import BASE_URL


class cdn_Crud:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        if(get_user_cred(kwargs['alias'])):
            self.API_key=get_user_cred(kwargs['alias'])[1]
            self.Auth_Token=get_user_cred(kwargs['alias'])[0]
            self.possible=True
        else:
            self.possible=False
        

    def create_cdn(self):
        Py_version_manager.py_print("Currently not integrated")
        # my_payload= {}  
        # cdn_name=Py_version_manager.py_input("input name of your new cdn : ")
        # while(Checks.cdn_name_validity(cdn_name)):
        #         cdn_name=Py_version_manager.py_input("Only following chars are supported: lowercase letters (a-z) or numbers(0-9)  Re-enter : ")

        # API_key=self.API_key
        # Auth_Token=self.Auth_Token
        # url =  BASE_URL+"myaccount/api/v1/storage/cdns/"+ cdn_name +"/?apikey="+API_key+"&location=Delhi"
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


    def delete_cdn(self):
        my_payload={}
        query=dict()
        query['domain_id']=Checks.take_input(self.kwargs["inputs"], "domain_id")
        API_key=self.API_key
        Auth_Token=self.Auth_Token
        url =  BASE_URL+"myaccount/api/v1/cdn/distributions/?apikey="+API_key
        req="DELETE"
        status=Request(url, Auth_Token, my_payload, req, query=query).response.json()

        if Checks.status_result(status,req):
                        Py_version_manager.py_print("CDN Successfully deleted")
                        Py_version_manager.py_print("use following command -> e2e_cli <alias> cdn list to check if cdn has been deleted")
        
        Checks.show_json(status)


    def list_cdn(self):
        my_payload={}
        API_key= self.API_key  
        Auth_Token= self.Auth_Token 
        url =  BASE_URL+"myaccount/api/v1/cdn/distributions/?apikey="+ API_key
        req="GET"
        status=Request(url, Auth_Token, my_payload, req).response.json()
        
        if Checks.status_result(status, req):
                Py_version_manager.py_print("Your cdns : ")
                try:
                    list=status['data']
                    i=1
                    x = PrettyTable()
                    x.field_names = ["index", "ID", "user_domain_name", "Created at", "domain_id"]
                    for element in list:
                        x.add_row([i, element['id'], element['user_domain_name'], element['created_at'], element['domain_id']])
                        i = i+1
                    Py_version_manager.py_print(x)
                except Exception as e:
                    Py_version_manager.py_print("Errors : ", e)
                    
        if('json' in self.kwargs["inputs"]):
            Checks.show_json(status)
    

