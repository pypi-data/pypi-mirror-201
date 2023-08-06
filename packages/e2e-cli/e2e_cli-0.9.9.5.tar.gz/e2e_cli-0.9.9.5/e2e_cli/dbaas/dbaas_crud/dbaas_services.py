import json
import re

from prettytable import PrettyTable


from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.core.alias_service import AliasServices
from e2e_cli.core.request_service import Request
from e2e_cli.core.helper_service import Checks
from e2e_cli.core.constants import BASE_URL



class DBaaSServices:
    def __init__(self, alias):
        self.alias = alias
        self.alias_service_object = AliasServices(alias)

    def all_dbaas(self):
        api_key_credentials_object = self.alias_service_object.get_api_credentials()
        if api_key_credentials_object["message"] == "Invalid alias provided":
            return api_key_credentials_object
        else:
            url =  BASE_URL+"myaccount/api/v1/rds/cluster/?apikey=" + \
                  api_key_credentials_object["api_credentials"]["api_key"] + "&location=Delhi"
            payload = {}
            Auth_Token= api_key_credentials_object["api_credentials"]["api_auth_token"]

            response = json.loads(Request(req="GET", url=url,  Auth_Token=Auth_Token, payload=payload).response.content)

            return {"dbaas_api_response": response,
                    "message": api_key_credentials_object["message"]}


    def password_validate(self, password):
        if not password.islower() and not password.isupper() and len(password)>=16 and bool(re.search(r'\d', password)) and \
                any(not c.isalnum() for c in password):
            return False
        else:
            return True
        
    def select_a_software(self, api_key, api_auth_token):
        url =  BASE_URL+"myaccount/api/v1/rds/plans/?apikey=" + api_key
        payload = {}
        Auth_Token= api_auth_token
        response =  Request(req="GET", url=url, Auth_Token=Auth_Token, payload=payload).response.json()
        if 'responseCode' in response:
            if "No client" in response["message"]:
                Py_version_manager.py_print("No Client found for this api credentials")
                return "/" 
        software_engines = response["data"]["database_engines"]
        table = PrettyTable(["Software ID", "Software Name", "Software Version"])
        for software_instance in software_engines:
            table.add_row([software_instance["id"], software_instance["name"], software_instance["version"]])
        Py_version_manager.py_print(table)
        software_id = Py_version_manager.py_input(": ")
        while(not Checks.is_int(software_id) or not 0<int(software_id)<=len(software_engines)):
            Py_version_manager.py_print("Please select one of above only")
            software_id = Py_version_manager.py_input(": ")
        software_id=int(software_id)
        return software_engines[software_id-1]["id"]
    
    def select_a_template(self, software_id, api_key, api_auth_token):
        url =  BASE_URL+"myaccount/api/v1/rds/plans/?apikey=" + api_key + "&software_id=" + str(software_id)
        payload = {}
        Auth_Token= api_auth_token
        response =  Request(req="GET", url=url, Auth_Token=Auth_Token, payload=payload).response.json()
        template_engines = response["data"]["template_plans"]
        table = PrettyTable(["Template ID", "Template Name", "Template Price"])
        templates_id = 1
        for template_instance in template_engines:
            table.add_row([templates_id, template_instance["name"], template_instance["price"]])
            templates_id+=1
        Py_version_manager.py_print(table)
        template_id_choice = int(Py_version_manager.py_input(": "))
        while(not Checks.is_int(template_id_choice) or not 0<int(template_id_choice)<=len(template_engines)):
            Py_version_manager.py_print("Please select one of above only")
            template_id_choice = Py_version_manager.py_input(": ")
        template_id_choice=int(template_id_choice)
        return template_engines[template_id_choice-1]["template_id"]
    

    def add_dbaas(self):
        Py_version_manager.py_print("Fill in the details required")
        Py_version_manager.py_print("(Note: All the fields having a important ahead of them can't be skipped)")
        name_assigned_to_database = Py_version_manager.py_input("Name of your database(important): ")
        while(name_assigned_to_database=="" or " " in name_assigned_to_database):
            name_assigned_to_database = Py_version_manager.py_input("Re-enter, name can't have spaces :")
        username_assigned_to_database = Py_version_manager.py_input("Assign UserName to your database(important): ")
        while(username_assigned_to_database=="" or " " in username_assigned_to_database):
            username_assigned_to_database = Py_version_manager.py_input("Re-enter, username can't have spaces :")
        password_assigned_to_database = Py_version_manager.py_input("Assign Password to your database(important): ")
        while self.password_validate(password_assigned_to_database):
            Py_version_manager.py_print("  You need to correct your password")
            Py_version_manager.py_print("Your Password should be of minimum 16 characters long. It should contain a number, an uppercase,"
                  "a lowercase, and a special character")
            password_assigned_to_database = Py_version_manager.py_input("Assign Password to your database(important): ")
        group_assigned_to_database = bool(Py_version_manager.py_input("Assign Group to your database(if you skip this field a "
                                                "Default Group will be assigned to your database): ")) or "Default"
        api_key_credentials_object = self.alias_service_object.get_api_credentials()
        if api_key_credentials_object["message"] == "Invalid alias provided":
            return api_key_credentials_object
        else:
            software_id = self.select_a_software(api_key_credentials_object["api_credentials"]["api_key"],
                                                 api_key_credentials_object["api_credentials"]["api_auth_token"])
            if software_id == '/':
                return None
            else:
                template_id = self.select_a_template(software_id, api_key_credentials_object["api_credentials"]["api_key"],
                                                    api_key_credentials_object["api_credentials"]["api_auth_token"])
                url =  BASE_URL+"myaccount/api/v1/rds/cluster/?apikey=" + \
                    api_key_credentials_object["api_credentials"]["api_key"] + "&location=Delhi"

                payload = json.dumps({
                    "database": {
                        "name": name_assigned_to_database,
                        "password": password_assigned_to_database,
                        "user": username_assigned_to_database
                    },
                    "group": group_assigned_to_database,
                    "name": name_assigned_to_database,
                    "software_id": software_id,
                    "template_id": template_id,
                })

                Auth_Token= api_key_credentials_object["api_credentials"]["api_auth_token"]
                response = Request(req="POST", url=url, Auth_Token=Auth_Token, payload=payload).response.json()

                return {"dbaas_api_response": response,
                        "message": api_key_credentials_object["message"]}


    def delete_dbaas(self):
        database_id = Py_version_manager.py_input("Enter the id of the database: ")
        while(not Checks.is_int(database_id)):
            database_id = Py_version_manager.py_input("Enter a valid id : ") 
        Py_version_manager.py_print("Load Balancing Property: ")
        Py_version_manager.py_print("Deleting this dbaas instance can cause data loss!")
        choice = Py_version_manager.py_input("Do you still want to continue?(Y/N)")
        if choice.upper() == "Y":
            api_key_credentials_object = self.alias_service_object.get_api_credentials()
            if api_key_credentials_object["message"] == "Invalid alias provided":
                return api_key_credentials_object
            else:

                url =  BASE_URL+"myaccount/api/v1/rds/cluster/" + database_id + "/?apikey=" + \
                      api_key_credentials_object["api_credentials"]["api_key"]

                payload = {}
            
                Auth_Token= api_key_credentials_object["api_credentials"]["api_auth_token"]
                response = Request(req="DELETE", url=url, Auth_Token=Auth_Token, payload=payload).response.json()

                if(not response["code"]==200):
                        Py_version_manager.py_print(response['errors'])
                        return {"message": "Failure"}
                else:      
                    return {"dbaas_api_response": response,
                            "message": api_key_credentials_object["message"]}
        else:
            return {"message": "Aborted"}
