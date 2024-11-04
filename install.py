#!/usr/bin/env python3

import sys
import ast
import importlib.util
import subprocess

def get_imported_modules(filename):
    """Parse the given Python file to find imported modules."""
    with open(filename, "r") as file:
        tree = ast.parse(file.read(), filename=filename)

    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name.split('.')[0])  # Get the top-level package name
        elif isinstance(node, ast.ImportFrom):
            imports.add(node.module.split('.')[0])  # Get the top-level package name

    return list(imports)

def is_module_installed(module_name):
    """Check if a Python module is installed."""
    spec = importlib.util.find_spec(module_name)
    return spec is not None

def generate_install_script(modules, script_filename="install_missing_dependencies.sh"):
    """Generate a shell script to install missing dependencies."""
    with open(script_filename, "w") as script:
        script.write("#!/bin/bash\n")
        script.write("echo 'Installing missing dependencies...'\n")
        for module in modules:
            script.write(f"sudo apt install -y python3-{module}\n")
    subprocess.run(["chmod", "+x", script_filename])  # Make the script executable
    print(f"Install script generated: {script_filename}")

def main(filename):
    imported_modules = get_imported_modules(filename)
    missing_modules = [module for module in imported_modules if not is_module_installed(module)]

    if not missing_modules:
        print("All dependencies are already installed.")
    else:
        print(f"Missing modules: {missing_modules}")
        generate_install_script(missing_modules)

# Run the main function on the specified Python file
filename_to_check = sys.argv[1] #"your_script.py"  # Change this to your target file
main(filename_to_check)

