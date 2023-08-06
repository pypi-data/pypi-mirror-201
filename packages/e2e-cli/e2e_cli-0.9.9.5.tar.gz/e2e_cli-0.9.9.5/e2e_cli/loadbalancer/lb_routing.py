import subprocess

from e2e_cli.core.py_manager import Py_version_manager 
from e2e_cli.loadbalancer.lb import LBClass


class LBRouting:
    def __init__(self, arguments):
        self.arguments = arguments

    def route(self, Parsing_Errors):
        if self.arguments.args.lb_commands is None:
            subprocess.call(['e2e_cli', 'lb', '-h'])


        elif(self.arguments.args.lb_commands is not None):
            lb_class_object = LBClass(alias=self.arguments.args.alias, inputs=self.arguments.inputs)
            
            if self.arguments.args.lb_commands == 'create':
                try:
                    lb_class_object.create_lb()
                except KeyboardInterrupt:
                    Py_version_manager.py_print(" ")
                
            elif self.arguments.args.lb_commands == 'list' or self.arguments.args.lb_commands == 'ls':
                try:
                    lb_class_object.list_lb()
                except KeyboardInterrupt:
                    Py_version_manager.py_print(" ")
                
            elif self.arguments.args.lb_commands == 'delete':
                try:
                    lb_class_object.delete_lb()
                except KeyboardInterrupt:
                    Py_version_manager.py_print(" ")
                
            elif self.arguments.args.lb_commands == 'edit':
                try:
                    lb_class_object.edit_lb()
                except KeyboardInterrupt:
                    Py_version_manager.py_print(" ")
                