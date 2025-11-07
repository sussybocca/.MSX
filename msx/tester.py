# tester.py
import os
import time
from ..runner import run_msx_file

def test_extension(path):
    if not os.path.exists(path):
        print(f"Error: Extension folder '{path}' does not exist.")
        return

    print(f"Testing extension: {path}")
    
    # Gather all .msx files in folder and subfolders
    msx_files = []
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(".msx"):
                msx_files.append(os.path.join(root, file))

    # Store last modification times for auto-reload
    last_mod_times = {file: os.path.getmtime(file) for file in msx_files}

    while True:
        for file in msx_files:
            try:
                print(f"\nRunning: {file}")
                run_msx_file(file)
            except Exception as e:
                print(f"Error in {file}: {e}")
        
        # Check for file changes
        changed = False
        for file in msx_files:
            mod_time = os.path.getmtime(file)
            if mod_time != last_mod_times[file]:
                last_mod_times[file] = mod_time
                changed = True
        if changed:
            print("\nChanges detected. Retesting...")
        else:
            print("\nAll tests completed successfully.")
            break
        
        time.sleep(1)  # Wait a bit before re-running
