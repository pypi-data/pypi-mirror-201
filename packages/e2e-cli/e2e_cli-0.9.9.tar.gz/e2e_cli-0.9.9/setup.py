import subprocess
try:
  from setuptools import setup, find_packages
except ImportError:
  subprocess.call["pip","install","setuptools"]
  from setuptools import setup, find_packages

setup(
    name='e2e_cli',
    version='0.9.9',
    description="This a E2E CLI tool for myAccount",
    author="Sajal&Aman@E2E_Networks_Ltd",
    packages=find_packages(),
    install_requires=['prettytable', 'requests', 'setuptools', 'chardet'],

    include_package_data = True,
    package_data = {
        '': ['*.1'],
        '': ['docs/*.1'],
        'docs': ['*.1'],
    },

    entry_points={
        'console_scripts': [
            'e2e_cli=e2e_cli.main:run_main_class'
        ]
    },
)

# from  install_man import runcls
# runcls().run()