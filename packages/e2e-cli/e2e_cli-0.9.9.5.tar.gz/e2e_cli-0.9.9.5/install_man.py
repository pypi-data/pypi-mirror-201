import os, platform
import subprocess


class runcls:
    def run(self):
        
        if platform.system() != "Windows":
            MAN_DIR = "/usr/local/share/man/man1"
            man_file = os.path.join(os.path.dirname(__file__), "e2e_cli/docs/e2e_cli.1")
            subprocess.call(["sudo", "cp", man_file, MAN_DIR])
            # subprocess.call(["sudo", "gzip", os.path.join(MAN_DIR, "e2e_cli/docs/e2e_cli.1")])
        