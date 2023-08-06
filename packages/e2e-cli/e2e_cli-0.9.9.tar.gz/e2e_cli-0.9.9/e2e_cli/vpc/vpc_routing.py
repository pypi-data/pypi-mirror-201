import subprocess

from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.vpc.vpc import vpc_Crud

class vpc_Routing:
    def __init__(self, arguments):
        self.arguments = arguments
        
        
    def route(self, Parsing_Errors):
        if (self.arguments.args.vpc_commands is None):
            subprocess.call(['e2e_cli', 'alias', 'vpc', '-h'])


        elif (self.arguments.args.vpc_commands is not None) and (self.arguments.args.action is not None):
            Py_version_manager.py_print("Only one action at a time !!")


        elif (self.arguments.args.vpc_commands is not None):
            vpc_operations = vpc_Crud(alias=self.arguments.args.alias, inputs=self.arguments.inputs)
            if(vpc_operations.possible):  

                if self.arguments.args.vpc_commands == 'create':
                                try:
                                    vpc_operations.create_vpc()
                                except KeyboardInterrupt:
                                    Py_version_manager.py_print(" ")

                elif self.arguments.args.vpc_commands == 'delete':
                    vpc_operations = vpc_Crud(alias=self.arguments.args.alias, inputs=self.arguments.inputs)
                    if(vpc_operations.possible):
                                try:
                                    vpc_operations.delete_vpc()
                                except KeyboardInterrupt:
                                    Py_version_manager.py_print(" ")
                                
                elif self.arguments.args.vpc_commands == 'list':
                    vpc_operations = vpc_Crud(alias=self.arguments.args.alias, inputs=self.arguments.inputs)
                    if(vpc_operations.possible):
                                try:
                                    vpc_operations.list_vpc()
                                except KeyboardInterrupt:
                                    Py_version_manager.py_print(" ")
        

        else:
            Py_version_manager.py_print("command not found")
            Py_version_manager.py_print(*Parsing_Errors, sep="\n")