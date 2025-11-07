#!/usr/bin/env python
import sys
import os
import subprocess
import tempfile
from runner import run_msx_file  # keeps MSX logic for .msx files

def main():
    if len(sys.argv) < 2:
        print("Usage: msx <script_or_msx_file> [args...]")
        sys.exit(1)

    target = sys.argv[1]
    args = sys.argv[2:]

    # If the file ends with .msx, run it with our runner
    if target.endswith(".msx"):
        if not os.path.exists(target):
            print(f"Error: MSX file '{target}' not found")
            sys.exit(1)
        run_msx_file(target)

    # If the file ends with .py, run it as a normal Python script
    elif target.endswith(".py"):
        if not os.path.exists(target):
            print(f"Error: Python script '{target}' not found")
            sys.exit(1)
        # Pass all extra arguments to the script
        subprocess.run([sys.executable, target, *args])

    else:
        # If not a file, treat it as a single MSX command
        with tempfile.NamedTemporaryFile("w+", suffix=".msx", delete=False) as tmp:
            tmp.write(target + "\n")
            tmp_path = tmp.name
        run_msx_file(tmp_path)
        os.remove(tmp_path)

if __name__ == "__main__":
    main()
