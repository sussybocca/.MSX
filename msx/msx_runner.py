# msx_runner.py - real interpreter for .msx scripts
import sys
import re

file_path = sys.argv[1]

# Store defined functions
functions = {}

# Read file
with open(file_path, "r") as f:
    lines = f.readlines()

# Simple parser for .msx
for line in lines:
    line = line.strip()
    if not line or line.startswith("#"):
        continue  # skip empty lines and comments

    # Print command: print "text"
    match = re.match(r'^print\s+"(.*)"$', line)
    if match:
        print(match.group(1))
        continue

    # Function definition: function name(arg) { ... }
    match = re.match(r'^function\s+(\w+)\((.*?)\)\s*{$', line)
    if match:
        func_name = match.group(1)
        arg_names = [arg.strip() for arg in match.group(2).split(",") if arg.strip()]
        functions[func_name] = {"args": arg_names, "body": []}
        current_func = func_name
        continue

    # End of function
    if line == "}":
        current_func = None
        continue

    # Add lines to function body
    if 'current_func' in locals() and current_func:
        functions[current_func]["body"].append(line)
        continue

    # Call function: call name(args)
    match = re.match(r'^call\s+(\w+)\((.*?)\)$', line)
    if match:
        func_name = match.group(1)
        args = [arg.strip('"') for arg in match.group(2).split(",") if arg.strip()]
        func = functions.get(func_name)
        if not func:
            print(f"Error: function {func_name} not defined")
            sys.exit(1)
        # Map args
        local_vars = dict(zip(func["args"], args))
        # Execute body
        for body_line in func["body"]:
            body_line = body_line.strip()
            match_print = re.match(r'^print\s+"(.*)"$', body_line)
            if match_print:
                text = match_print.group(1)
                # Replace variables in text
                for var, val in local_vars.items():
                    text = text.replace(f"${var}", val)
                print(text)
        continue

    print(f"Unknown command: {line}")
