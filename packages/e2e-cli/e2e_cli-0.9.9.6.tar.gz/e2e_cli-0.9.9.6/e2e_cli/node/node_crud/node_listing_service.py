from prettytable import PrettyTable

from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.core.alias_service import get_user_cred
from e2e_cli.core.request_service import Request
from e2e_cli.core.constants import BASE_URL


class Nodelisting:
    def __init__(self, alias):
        if (get_user_cred(alias)):
            self.API_key = get_user_cred(alias)[1]
            self.Auth_Token = get_user_cred(alias)[0]


    def node_listing(self):
        url =  BASE_URL+"myaccount/api/v1/images/category-list/?apikey=" +self.API_key+ "&contact_person_id=null&location=Delhi"
        req= "GET"
        my_payload={}
        response= Request(url, self.Auth_Token, my_payload, req, user_agent='cli_python').response.json()['data']

        i=1
        x=PrettyTable()
        x.field_names=["ID", 'Types of node']
        category=dict()
        for key in response['category_list']:
                x.add_row([i, key])
                category[str(i)]=key
                i=i+1
        Py_version_manager.py_print(x)
        node_type= Py_version_manager.py_input("Select one of above id : ")
        while(not node_type in category):
              node_type= Py_version_manager.py_input("Select one of above id : ")
        node_type=category[node_type]
        
        i=1
        x=PrettyTable()
        x.field_names=["ID", 'Types of OS']
        Os_type_list=dict()
        for key in response['category_list'][node_type]:
                x.add_row([i, key])
                Os_type_list[str(i)]=key
                i=i+1
        Py_version_manager.py_print(x)
        Os_type= Py_version_manager.py_input("Select one of above id : ")
        while(not Os_type in Os_type_list):
              Os_type= Py_version_manager.py_input("Select one of above id : ")
        Os_type= Os_type_list[Os_type]

        i=1
        x=PrettyTable()
        x.field_names=["ID", 'Types of OS']
        Os_version_list=dict()
        for key in response['category_list'][node_type][Os_type]:
                x.add_row([i, key['version']])
                Os_version_list[str(i)]=key['version']
                i=i+1
        Py_version_manager.py_print(x)
        Os_version= Py_version_manager.py_input("Select one of above id : ")
        while(not Os_version in Os_version_list):
              Os_version= Py_version_manager.py_input("Select one of above id : ")
        Os_version= Os_version_list[Os_version]

        node_type=node_type.split()
        node_type1=""
        for ele in node_type:
              node_type1=node_type1+ele+"%20"
      
      

        url =  BASE_URL+"myaccount/api/v1/images/?apikey="+ self.API_key+"&contact_person_id=null&display_category="+node_type1 +"&category="+Os_type +"&osversion="+Os_version +"&gpu_type=&ng_container=null&os="+Os_type +"&location=Delhi"
        req= "GET"
        my_payload={}
        response= Request(url, self.Auth_Token, my_payload, req, user_agent='cli_python').response.json()['data']
        i=1
        x=PrettyTable()
        x.field_names=["ID", 'Plan', 'image', 'location', 'Price(Monthly)', 'Price(Hourly)']
        Plan_list=dict()
        for key in response:
                x.add_row([i, key['plan'], key['image'], key['location'], key['specs']['price_per_month'], key['specs']['price_per_hour'] ] )
                Plan_list[str(i)]= dict(plan= key['plan'], image=key['image'], location=key['location'])
                i=i+1
        Py_version_manager.py_print(x)
        choice=Py_version_manager.py_input("Enter your choice")
        while(not choice in Plan_list):
              choice=Py_version_manager.py_input("Select one of above id : ")
        return Plan_list[choice]