import subprocess

from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.cdn.cdn_crud.cdn import cdn_Crud
from e2e_cli.cdn.cdn_actions.cdn_action import cdnActions

class cdn_Routing:
    def __init__(self, arguments):
        self.arguments = arguments
        
        
    def route(self, Parsing_Errors):
        if (self.arguments.args.action is None) and (self.arguments.args.cdn_commands is None):
            subprocess.call(['e2e_cli', 'cdn', '-h'])


        elif (self.arguments.args.cdn_commands is not None) and (self.arguments.args.action is not None):
              Py_version_manager.py_print("Only one action at a time !!")


        elif(self.arguments.args.cdn_commands is not None):
            cdn_operations = cdn_Crud(alias=self.arguments.args.alias, inputs=self.arguments.inputs)
            if(cdn_operations.possible):

                if self.arguments.args.cdn_commands == 'create':
                        try:
                            cdn_operations.create_cdn()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")

                elif self.arguments.args.cdn_commands == 'delete':
                        try:
                            cdn_operations.delete_cdn()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
                        
                elif self.arguments.args.cdn_commands == 'list':
                        try:
                            cdn_operations.list_cdn()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")


        elif(self.arguments.args.action is not None):
            cdn_operations = cdnActions(alias=self.arguments.args.alias, inputs=self.arguments.inputs)
            if(cdn_operations.possible):
                
                if self.arguments.args.action == "enable_cdn":
                        try:
                            cdn_operations.enable_cdn()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")

                elif self.arguments.args.action == "disable_cdn":
                        try:
                            cdn_operations.disable_cdn()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
                
                elif self.arguments.args.action == "cdn_monitoring":
                        try:
                            cdn_operations.cdn_monitoring()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")

                elif self.arguments.args.action == "cdn_bandwidth_usage":
                        try:
                            cdn_operations.cdn_bandwidth_usage()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
        

        else:
            Py_version_manager.py_print("command not found")
            Py_version_manager.py_print(*Parsing_Errors, sep="\n")