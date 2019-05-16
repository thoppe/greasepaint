from fabric.api import local

exclude_command = ""

def watch():
    local("rm -rf static/")
    local("python miniprez watch index.md")
