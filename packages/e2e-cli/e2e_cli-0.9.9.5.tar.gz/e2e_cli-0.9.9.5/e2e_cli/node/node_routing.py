import subprocess

from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.node.node_crud.node import NodeCrud
from e2e_cli.node.node_actions.node_action import nodeActions

class NodeRouting:
    def __init__(self, arguments):
        self.arguments = arguments
        

    def route(self, Parsing_Errors):
        if (self.arguments.args.node_commands is None) and (self.arguments.args.action is None):
            subprocess.call(['e2e_cli','node', '-h'])


        elif (self.arguments.args.node_commands is not None) and (self.arguments.args.action is not None):
              Py_version_manager.py_print("Only one action at a time !!")


        elif(self.arguments.args.node_commands is not None):
            Node_operations = NodeCrud(alias=self.arguments.args.alias, inputs=self.arguments.inputs)
            if(Node_operations.possible):

                if self.arguments.args.node_commands == 'create':
                        try:
                            Node_operations.create_node()
                        except KeyboardInterrupt:
                                Py_version_manager.py_print(" ")  
                            

                elif self.arguments.args.node_commands == 'delete':
                        try:
                            Node_operations.delete_node()
                        except KeyboardInterrupt:
                                Py_version_manager.py_print(" ")
                        

                elif self.arguments.args.node_commands == 'get':
                        try:
                            Node_operations.get_node_by_id()
                        except KeyboardInterrupt:
                                Py_version_manager.py_print(" ")
                            
                                            
                elif self.arguments.args.node_commands == 'list':
                        try: 
                            Node_operations.list_node()
                        except KeyboardInterrupt:
                                Py_version_manager.py_print(" ")
                        

        elif(self.arguments.args.action is not None):
            Node_operations=nodeActions(alias=self.arguments.args.alias, inputs=self.arguments.inputs) 
            if(Node_operations.possible):

                if self.arguments.args.action == 'enable_recovery':  
                        try: 
                           Node_operations.enable_recovery()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
            
                elif self.arguments.args.action == 'disable_recovery':  
                        try: 
                           Node_operations.disable_recovery()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
            
                elif self.arguments.args.action == 'reinstall':  
                        try: 
                           Node_operations.reinstall()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
            
                elif self.arguments.args.action == 'reboot':  
                        try: 
                           Node_operations.reboot()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
            
                elif self.arguments.args.action == 'power_on':  
                        try: 
                           Node_operations.power_on()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
            
                elif self.arguments.args.action == 'power_off':  
                        try: 
                           Node_operations.power_off()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
            
                elif self.arguments.args.action == 'rename_node':  
                        try: 
                           Node_operations.rename_node()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
            
                elif self.arguments.args.action == 'lock_vm':  
                        try: 
                           Node_operations.lock_vm()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
            
                elif self.arguments.args.action == 'unlock_vm':  
                        try: 
                           Node_operations.unlock_vm()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
            
                elif self.arguments.args.action =='monitor':
                        try: 
                           Node_operations.node_monitoring()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
                
                else:
                    Py_version_manager.py_print("command not found")
                    Py_version_manager.py_print(*Parsing_Errors, sep="\n")


        else:
            Py_version_manager.py_print("command not found")
            Py_version_manager.py_print(*Parsing_Errors, sep="\n")