# signer.py
import os
import json
import secrets
import string
import shutil

BLACKLISTED_PATTERNS = ["os.remove", "subprocess", "eval(", "exec(", "open("]

def scan_file_for_malicious_code(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            for pattern in BLACKLISTED_PATTERNS:
                if pattern in line:
                    return f"Malicious pattern '{pattern}' found in {filepath} line {i}"
    return None

def sign_extension(extension_path):
    if not os.path.exists(extension_path):
        print(f"Error: Extension folder '{extension_path}' not found.")
        return

    # Scan all supported files
    for root, _, files in os.walk(extension_path):
        for file in files:
            if file.endswith((".msx", ".py", ".js", ".json")):
                filepath = os.path.join(root, file)
                error = scan_file_for_malicious_code(filepath)
                if error:
                    print(f"Malicious code detected: {error}")
                    print("Deleting extension for safety...")
                    shutil.rmtree(extension_path)
                    return

    # Safe: generate API key and connection string
    api_key = "".join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))
    connection_string = "".join(secrets.choice(string.ascii_letters + string.digits) for _ in range(64))

    # Update extension.config.js
    config_file = os.path.join(extension_path, "extension.config.js")
    with open(config_file, "w", encoding="utf-8") as f:
        f.write(f'MSX_API_EXTENSION = "{api_key}"\n')
        f.write(f'.msx MY_CONNECTION_STRING = "{connection_string}"\n')

    print(f"Extension '{extension_path}' signed successfully!")
    print(f"API Key: {api_key}")
    print(f"Connection String: {connection_string}")
    print(f"Please ensure you have extension.config.js updated in your extension folder.")
