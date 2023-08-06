import subprocess

from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.bucket_store.bucket_crud.bucket_storage import bucketCrud
from e2e_cli.bucket_store.bucket_actions.bucket_actions import BucketActions

class BucketRouting:
    def __init__(self, arguments):
        self.arguments = arguments
        
        
    def route(self, Parsing_Errors):
        if (self.arguments.args.bucket_commands is None) and (self.arguments.args.action is None):
            subprocess.call(['e2e_cli', 'bucket', '-h'])


        elif (self.arguments.args.bucket_commands is not None) and (self.arguments.args.action is not None):
              Py_version_manager.py_print("Only one action at a time !!")


        elif(self.arguments.args.bucket_commands is not None):
            bucket_operations = bucketCrud(alias=self.arguments.args.alias, inputs=self.arguments.inputs)
            if(bucket_operations.possible):
                
                if self.arguments.args.bucket_commands == 'create':
                                try:
                                    bucket_operations.create_bucket()
                                except KeyboardInterrupt:
                                    Py_version_manager.py_print(" ")

                elif self.arguments.args.bucket_commands == 'delete':
                                try:
                                    bucket_operations.delete_bucket()
                                except KeyboardInterrupt:
                                    Py_version_manager.py_print(" ")
                                
                elif self.arguments.args.bucket_commands == 'list':
                                try:
                                    bucket_operations.list_bucket()
                                except KeyboardInterrupt:
                                    Py_version_manager.py_print(" ")


        elif(self.arguments.args.action is not None):
            Bucket_operations=BucketActions(alias=self.arguments.args.alias, inputs=self.arguments.inputs)     
            if(Bucket_operations.possible):

                if self.arguments.args.action == 'enable_versioning':
                        try: 
                           Bucket_operations.enable_versioning()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
                        
                elif self.arguments.args.action == 'disable_versioning':
                        try: 
                           Bucket_operations.disable_versioning()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
                        
                elif self.arguments.args.action == 'create_key':
                        try: 
                           Bucket_operations.create_key()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")

                elif self.arguments.args.action == 'delete_key':
                        try: 
                           Bucket_operations.delete_key()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
        
                elif self.arguments.args.action == 'list_key':
                        try: 
                           Bucket_operations.list_key()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
                            
                elif self.arguments.args.action == 'lock_key':
                        try: 
                           Bucket_operations.lock_key()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
        
                elif self.arguments.args.action == 'unlock_key':
                        try: 
                           Bucket_operations.unlock_key()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")

                elif self.arguments.args.action == 'add_permission':
                        try: 
                           Bucket_operations.add_permission()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
        

        else:
            Py_version_manager.py_print("command not found")
            Py_version_manager.py_print(*Parsing_Errors, sep="\n")