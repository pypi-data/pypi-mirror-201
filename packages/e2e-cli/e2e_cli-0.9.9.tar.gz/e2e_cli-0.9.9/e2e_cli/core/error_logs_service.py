import json
import os
import platform
from datetime import datetime

from e2e_cli.core.py_manager import Py_version_manager

def action_on_exception(exception, alias, traceback):
    ErrorLogs(exception, alias, traceback).add_to_error_logs()


class ErrorLogs:
    def __init__(self, exception, alias, traceback):
        self.traceback=traceback
        self.exception=exception
        self.alias=alias
        self.home_directory = os.path.expanduser("~")
        if platform.system() == "Windows":
            self.folder= self.home_directory + "\.E2E_CLI"
            self.error_file= self.home_directory + "\.E2E_CLI\errors.json"
        elif platform.system() == "Linux" or platform.system() == "Darwin":
            self.folder= self.home_directory + "/.E2E_CLI"
            self.error_file= self.home_directory + "/.E2E_CLI/errors.json"


    def windows_hider(self):
        os.system("attrib +h " + self.folder)

    def windows_file_check(self):
        if not os.path.isdir(self.folder):
            return -1
        elif not os.path.isfile(self.error_file):
            self.windows_hider()
            return 0
        else:
            self.windows_hider()
            return 1

    def linux_mac_file_check(self):
        if not os.path.isdir(self.folder):
            return -1
        elif not os.path.isfile(self.error_file):
            return 0
        else:
            return 1
        
    def check_if_file_exist(self):
        if platform.system() == "Windows":
            return self.windows_file_check()
        elif platform.system() == "Linux" or platform.system() == "Darwin":
            return self.linux_mac_file_check()

    def save_error(self):
        error = {"date_time":str(datetime.now()), "alias":self.alias, "Exception_msg": str(self.exception), "traceback": self.traceback}

        with open(self.error_file, 'r+') as file_reference:
                read_string = file_reference.read()
                if read_string == "":
                    # print(error)
                    file_reference.write(json.dumps({"error_logs": [error]}))
                else:
                    error_logs = json.loads(read_string)['error_logs']
                    error_logs.append(error)
                    file_reference.seek(0)
                    file_reference.write(json.dumps({"error_logs": error_logs}))

    def add_to_error_logs(self):
        file_exist_check_variable = self.check_if_file_exist()
        if file_exist_check_variable == -1:
            os.mkdir(self.folder)
            with open(self.error_file, 'w'):
                pass
            self.save_error()
        else:
            with open(self.error_file, 'w'):
                pass
            self.save_error()

    @classmethod
    def recent_errors(self):
        if platform.system() == "Windows":
            error_file= os.path.expanduser("~") + "\.E2E_CLI\errors.json"
        elif platform.system() == "Linux" or platform.system() == "Darwin":
            error_file= os.path.expanduser("~") + "/.E2E_CLI/errors.json"

        try:
            with open(error_file, 'r+') as file_reference:
                    read_string = file_reference.read()
                    error_logs = json.loads(read_string)['error_logs']
                    Py_version_manager.py_print( error_logs[-1]['date_time'], error_logs[-1]['alias'])
                    Py_version_manager.py_print(error_logs[-1]['Exception_msg'], " : ")
                    for trace in error_logs[-1]['traceback'] :
                        Py_version_manager.py_print(trace)   
        except:
            Py_version_manager.py_print("Error logs not found")
