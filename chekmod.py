import ast
import subprocess
import sys

def install_module(module):
    try:
        # Check if module is already installed
        __import__(module)
        print(f"{module} is already installed")
    except ImportError:
        # Install module using pip
        print(f"Installing {module}...")
        subprocess.check_call(['pip', 'install', module])
        print(f"{module} has been installed")

def check_and_install_modules(filename):
    with open(filename, 'r') as file:
        tree = ast.parse(file.read())

    # Extract imported module names
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for name in node.names:
                imports.append(name.name)
        elif isinstance(node, ast.ImportFrom):
            imports.append(node.module)

    # Check and install required modules
    for module in imports:
        install_module(module)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please provide the Python file path as a command-line argument.")
        sys.exit(1)

    python_file = sys.argv[1]
    check_and_install_modules(python_file)
