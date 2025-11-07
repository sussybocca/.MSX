# extension.py
import os
import shutil

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "template")

def create_extension(name):
    # Check if the extension folder already exists
    if os.path.exists(name):
        print(f"Error: Folder '{name}' already exists.")
        return

    # Check if the template folder exists
    if not os.path.exists(TEMPLATE_DIR):
        print(f"Error: Template folder '{TEMPLATE_DIR}' does not exist!")
        return

    # Copy template to new extension folder
    shutil.copytree(TEMPLATE_DIR, name)
    print(f"Extension '{name}' created successfully at: {os.path.abspath(name)}")
    print("You can now edit the files and add your MSX code.")
