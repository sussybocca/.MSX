#!/usr/bin/env python
import sys
import os
import tempfile
from runner import run_msx_file  # Make sure runner.py is in the same folder

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  msx run <msx_file>     # Run an MSX script")
        print("  msx <command>          # Run a single MSX command directly")
        sys.exit(1)

    command_or_file = sys.argv[1]

    # If using "run", treat next argument as a file
    if command_or_file == "run":
        if len(sys.argv) < 3:
            print("Usage: msx run <msx_file>")
            sys.exit(1)
        msx_file = sys.argv[2]
        if not os.path.exists(msx_file):
            print(f"Error: File not found: {msx_file}")
            sys.exit(1)
        run_msx_file(msx_file)
        return

    # Otherwise, treat it as a single command typed inline
    temp_file = tempfile.NamedTemporaryFile("w+", suffix=".msx", delete=False)
    try:
        temp_file.write(command_or_file + "\n")
        temp_file.flush()
        temp_file.close()
        run_msx_file(temp_file.name)
    finally:
        os.remove(temp_file.name)

if __name__ == "__main__":
    main()
