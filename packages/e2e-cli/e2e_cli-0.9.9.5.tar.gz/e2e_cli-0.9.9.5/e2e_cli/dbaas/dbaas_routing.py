import subprocess

from e2e_cli.dbaas.dbaas_crud.dbaas import DBaaSClass
from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.dbaas.dbaas_actions.dbaas_action import DBaasAction



class DBaaSRouting:
    def __init__(self, arguments):
        self.arguments = arguments

    def route(self, Parsing_Errors):
        if (self.arguments.args.dbaas_commands is None) and (self.arguments.args.action is None):
            subprocess.call(['e2e_cli','dbaas', '-h'])


        elif (self.arguments.args.dbaas_commands is not None) and (self.arguments.args.action is not None):
              Py_version_manager.py_print("Only one action at a time !!")


        elif (self.arguments.args.dbaas_commands is not None):
            dbaas_class_object = DBaaSClass(alias=self.arguments.args.alias, inputs=self.arguments.inputs)

            if self.arguments.args.dbaas_commands == 'create':
                try:
                    dbaas_class_object.create_dbaas()
                except KeyboardInterrupt:
                    Py_version_manager.py_print(" ")

            elif self.arguments.args.dbaas_commands == 'list' or self.arguments.args.dbaas_commands == 'ls':
                try:
                    dbaas_class_object.list_dbaas()
                except KeyboardInterrupt:
                    Py_version_manager.py_print(" ")

            elif self.arguments.args.dbaas_commands == 'delete':
                try:
                    dbaas_class_object.delete_dbaas_by_name()
                except KeyboardInterrupt:
                    Py_version_manager.py_print(" ")
        

        elif(self.arguments.args.action is not None):
            DBaas_operations=DBaasAction(alias=self.arguments.args.alias, inputs=self.arguments.inputs)     
            if(DBaas_operations.possible):
            
                if self.arguments.args.action == 'take_snapshot':
                        try: 
                           DBaas_operations.take_snapshot()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
            
                elif self.arguments.args.action == 'reset_password':
                        try: 
                           DBaas_operations.reset_password()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
            
                elif self.arguments.args.action == 'stop_db':
                        try: 
                           DBaas_operations.stop_db()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
            
                elif self.arguments.args.action == 'start_db':
                        try: 
                           DBaas_operations.start_db()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
        
                elif self.arguments.args.action == 'restart_db':
                        try: 
                           DBaas_operations.restart_db()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
            
                elif self.arguments.args.action == 'enable_backup':
                        try: 
                           DBaas_operations.enable_backup()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
            
                elif self.arguments.args.action == 'disable_backup':
                        try: 
                           DBaas_operations.disable_backup()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
        
                elif self.arguments.args.action == 'add_parameter_group':
                        try: 
                           DBaas_operations.add_parameter_group()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
            
                elif self.arguments.args.action == 'remove_parameter_group':
                        try: 
                           DBaas_operations.remove_parameter_group()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
            
                elif self.arguments.args.action == 'add_vpc':
                        try: 
                           DBaas_operations.add_vpc()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
            
                elif self.arguments.args.action == 'remove_vpc':
                        try: 
                           DBaas_operations.remove_vpc()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
        

        else:
            Py_version_manager.py_print("command not found")
            Py_version_manager.py_print(*Parsing_Errors, sep="\n")