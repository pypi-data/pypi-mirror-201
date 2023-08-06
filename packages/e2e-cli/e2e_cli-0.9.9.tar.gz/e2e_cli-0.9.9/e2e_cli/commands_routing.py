import subprocess

from e2e_cli.core.error_logs_service import action_on_exception
from e2e_cli.core.helper_service import Checks
from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.core import help_messages

from e2e_cli.config.config_routing import ConfigRouting
from e2e_cli.loadbalancer.lb_routing import LBRouting
from e2e_cli.node.node_routing import NodeRouting
from e2e_cli.bucket_store.bucket_routing import BucketRouting
from e2e_cli.dbaas.dbaas_routing import DBaaSRouting
from e2e_cli.image.image_routing import ImageRouting
from e2e_cli.auto_scaling.autoscaling_routing import autoscaling_Routing
from e2e_cli.cdn.cdn_routing import cdn_Routing
from e2e_cli.vpc.vpc_routing import vpc_Routing
from e2e_cli.volumes.volumes_routing import volumes_Routing
from e2e_cli.man_display import man_page

class CommandsRouting:
    def __init__(self, arguments):
        self.arguments = arguments

    def route(self, Parsing_Errors):

        if(self.arguments.args.version):
              help_messages.e2e_version_info()


        elif(self.arguments.args.info):
              help_messages.e2e_pakage_info()


        elif self.arguments.args.command is None:
                subprocess.call(['e2e_cli', "-h"])


        elif self.arguments.args.command == "help" or self.arguments.args.command == "doc":
                man_page()


        elif (self.arguments.args.command == "alias") :

            if self.arguments.args.alias_commands in ["add", "view", "add_file", "delete", "set"]:
                try:
                    ConfigRouting(self.arguments).route(Parsing_Errors)
                except Exception as e:
                    if("debug" in self.arguments.inputs):
                                Checks.manage_exception(e)
                                # action_on_exception(e, self.arguments.args.alias, traceback.print_exc())
            else:

                Py_version_manager.py_print(*Parsing_Errors, sep="\n")
                subprocess.call(['e2e_cli', "alias","-h"])
    
    
        else:
            if(self.arguments.args.alias=="default"):
                Py_version_manager.py_print("Using default alias")

            if self.arguments.args.command == "node":
                try:
                    NodeRouting(self.arguments).route(Parsing_Errors)
                except Exception as e:
                    if("debug" in self.arguments.inputs):
                                Checks.manage_exception(e)

            elif self.arguments.args.command == "lb":
                try: 
                    LBRouting(self.arguments).route(Parsing_Errors)
                except Exception as e:
                        if("debug" in self.arguments.inputs):
                                Checks.manage_exception(e)
                                # action_on_exception(e, self.arguments.args.alias, traceback.print_exc()) 
    
            elif self.arguments.args.command == "bucket":
                try:
                    BucketRouting(self.arguments).route(Parsing_Errors)
                except Exception as e:
                        if("debug" in self.arguments.inputs):
                                Checks.manage_exception(e)
                                # action_on_exception(e, self.arguments.args.alias, traceback.print_exc())
            
            elif self.arguments.args.command == "dbaas":
                try:
                    DBaaSRouting(self.arguments).route(Parsing_Errors)
                except Exception as e:
                        if("debug" in self.arguments.inputs):
                                Checks.manage_exception(e)
                                # action_on_exception(e, self.arguments.args.alias, traceback.print_exc())

            elif self.arguments.args.command == "image":
                try:
                    ImageRouting(self.arguments).route(Parsing_Errors)
                except Exception as e:
                            if("debug" in self.arguments.inputs):
                                Checks.manage_exception(e)
                            # action_on_exception(e, self.arguments.args.alias, traceback.print_exc())   

            elif self.arguments.args.command == "autoscaling":
                try:
                    autoscaling_Routing(self.arguments).route(Parsing_Errors)
                except Exception as e:
                            if("debug" in self.arguments.inputs):
                                Checks.manage_exception(e)
                            # action_on_exception(e, self.arguments.args.alias, traceback.print_exc())   
        
            elif self.arguments.args.command == "cdn":
                try:
                    cdn_Routing(self.arguments).route(Parsing_Errors)
                except Exception as e:
                            if("debug" in self.arguments.inputs):
                                Checks.manage_exception(e)
                            # action_on_exception(e, self.arguments.args.alias, traceback.print_exc()) 

            elif self.arguments.args.command == "vpc":
                try:
                    vpc_Routing(self.arguments).route(Parsing_Errors)
                except Exception as e:
                            if("debug" in self.arguments.inputs):
                                Checks.manage_exception(e)
                            # action_on_exception(e, self.arguments.args.alias, traceback.print_exc())  

            elif self.arguments.args.command == "volumes":
                try:
                    volumes_Routing(self.arguments).route(Parsing_Errors)
                except Exception as e:
                            if("debug" in self.arguments.inputs):
                                Checks.manage_exception(e)
                            # action_on_exception(e, self.arguments.args.alias, traceback.print_exc())  

            else:
                Py_version_manager.py_print("Command not found!! for more help type e2e_cli help")
                Py_version_manager.py_print(*Parsing_Errors, sep="\n")
        