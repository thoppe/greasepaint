import os

def lint():
    os.system("black greasepaint tests")
    #os.system("flake8 pyzulia/ --ignore=E501,E203 %s"%exclude_command)

def test():
    os.system("python -m pytest --workers auto tests/")

def clean():
    os.system("rm -rvf .tox *.egg-info")
