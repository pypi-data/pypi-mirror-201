from prettytable import PrettyTable

from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.dbaas.dbaas_crud.dbaas_services import DBaaSServices
from e2e_cli.core.helper_service import Checks

class DBaaSClass:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def list_dbaas(self):
        alias = self.kwargs["alias"]
        dbaas_services_object = DBaaSServices(alias)
        dbaas_service_response_object = dbaas_services_object.all_dbaas()
        if dbaas_service_response_object["message"] == "Valid alias":
            dbaas_api_response_object = dbaas_service_response_object["dbaas_api_response"]
            if dbaas_api_response_object["code"] == 200:
                table = PrettyTable(["Database ID", "Database Name", "Database Status",
                                     "Database Software",
                                     "Plan"])
                for database_instance in dbaas_api_response_object["data"]:
                    table.add_row([database_instance["id"], database_instance["name"],
                                   database_instance["status"], (database_instance["software"]["name"] +
                                                                 " " + database_instance["software"]
                                                                 ["version"]),
                                   ("Name-"+database_instance["master_node"]["plan"]['name'] +" Cpu"+database_instance["master_node"]["plan"]['cpu']+"_disk"+database_instance["master_node"]["plan"]['disk']) ])

                if table.rowcount == 0:
                    Py_version_manager.py_print("No database found. please create one using following command \
                    e2e_cli dbaas add <alias>")  
                    return 0                 

                Py_version_manager.py_print(table)
                Checks.show_json(dbaas_api_response_object)
                return 1

        else:
            Py_version_manager.py_print("Please provide a valid Alias")
            return 0

    def create_dbaas(self):
        alias = self.kwargs["alias"]
        dbaas_services_object = DBaaSServices(alias)
        dbaas_service_response_object = dbaas_services_object.add_dbaas()
        if dbaas_service_response_object is None:
            pass
        elif dbaas_service_response_object["message"] == "Valid alias":
            dbaas_api_response_object = dbaas_service_response_object["dbaas_api_response"]
            if dbaas_api_response_object["code"] == 200:
                dbaas_api_response_object_data = dbaas_api_response_object["data"]
                Py_version_manager.py_print("Name of the database    : ", dbaas_api_response_object_data["name"])
                Py_version_manager.py_print("Status of the database    : ", dbaas_api_response_object_data["status"])
                Py_version_manager.py_print("Database Software         : ", dbaas_api_response_object_data["software"]["name"] + " " +
                      dbaas_api_response_object_data["software"]["version"])
                Py_version_manager.py_print("Database Engine           : ", dbaas_api_response_object_data["software"]["engine"])
                Py_version_manager.py_print("Ram                       : ", dbaas_api_response_object_data["master_node"]["ram"])
                Py_version_manager.py_print("CPU                       : ", dbaas_api_response_object_data["master_node"]["cpu"])
                Py_version_manager.py_print("Disk                      : ", dbaas_api_response_object_data["master_node"]["disk"])
                Py_version_manager.py_print("Plan                      : ",
                      dbaas_api_response_object_data["master_node"]["plan"]["name"])
                Py_version_manager.py_print("Price                     : ",
                      dbaas_api_response_object_data["master_node"]["plan"]["price"])
                Py_version_manager.py_print("  Your Database instance is in " + dbaas_api_response_object_data["status"] + " state")
                Py_version_manager.py_print(
                    "To check the state of the database you can run e2e_cli dbaas list <alias> ")
                Checks.show_json(dbaas_api_response_object_data)

            else:
                Py_version_manager.py_print(dbaas_api_response_object["errors"])

        else:
            Py_version_manager.py_print("Please provide a valid Alias")

    def delete_dbaas_by_name(self):
        can_move_forward = self.list_dbaas()
        if can_move_forward == 0:
            pass
        else:
            alias = self.kwargs["alias"]
            dbaas_services_object = DBaaSServices(alias)
            dbaas_delete_response_object = dbaas_services_object.delete_dbaas()
            if dbaas_delete_response_object["message"] == "Valid alias":
                Py_version_manager.py_print("  Your instance have been deleted")
                Py_version_manager.py_print(
                         "To check the state of the database you can run e2e_cli dbaas list <alias> "
                )
            elif dbaas_delete_response_object["message"] == "Aborted":
                Py_version_manager.py_print(dbaas_delete_response_object["message"])
