import os
import re
import json
import time

# ===============================
# Subscription & rating storage
# ===============================
SUBS_FILE = "subs.msx"
RATINGS_FILE = "ratings.msx"
GHOST_FILE = "ghost.command-fig.json"

# ===============================
# Core MSX Runner
# ===============================
def run_msx_file(path, reset=False):
    """
    Executes a .msx file with support for:
    - print statements
    - function definitions and calls
    - MSX commands including rate, subscription, ghost, restart
    """
    if not os.path.exists(path):
        print(f"Error: File {path} not found.")
        return

    functions = {}
    current_func = None

    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        # MSX statements
        if line.startswith("msx "):
            handle_msx_statement(line)
            continue

        # function definition
        match = re.match(r'^function\s+(\w+)\((.*?)\)\s*{$', line)
        if match:
            func_name = match.group(1)
            args = [a.strip() for a in match.group(2).split(",") if a.strip()]
            functions[func_name] = {"args": args, "body": []}
            current_func = func_name
            continue

        # function end
        if line == "}":
            current_func = None
            continue

        # inside function body
        if current_func:
            functions[current_func]["body"].append(line)
            continue

        # call function
        match_call = re.match(r'^call\s+(\w+)\((.*?)\)$', line)
        if match_call:
            func_name = match_call.group(1)
            args_values = [arg.strip('"') for arg in match_call.group(2).split(",") if arg.strip()]
            func = functions.get(func_name)
            if not func:
                print(f"Error: Function '{func_name}' not defined at line {i+1}")
                return
            local_vars = dict(zip(func["args"], args_values))
            for body_line in func["body"]:
                handle_body_line(body_line, local_vars)
            continue

        # print statement
        match_print = re.match(r'^print\s+"(.*)"$', line)
        if match_print:
            print(match_print.group(1))
            continue

        print(f"Unknown command at line {i+1}: {line}")


# ===============================
# Function body execution
# ===============================
def handle_body_line(line, local_vars):
    line = line.strip()
    # print statements
    match_print = re.match(r'^print\s+"(.*)"$', line)
    if match_print:
        text = match_print.group(1)
        for var, val in local_vars.items():
            text = text.replace(f"${var}", val)
        print(text)
    # nested function call (optional)
    match_call = re.match(r'^call\s+(\w+)\((.*?)\)$', line)
    if match_call:
        print(f"Nested call detected but not executed: {line}")


# ===============================
# MSX Command Handler
# ===============================
def handle_msx_statement(line):
    line = line.strip()
    if line == "msx help":
        print("MSX Help: list of commands...")
    elif line == "msx export commands list":
        print("Exporting commands list...")
    elif line == "msx commands":
        print("Listing MSX commands...")
    elif line == "msx terminal":
        print("Opening MSX terminal...")
    elif line == "msx double click file commands":
        run_ghost_commands("double_click")
    elif line == "msx sign commands":
        print("Running sign commands...")
    elif line.startswith("msx extension import from file"):
        file = line.split()[-1]
        print(f"Importing extension from {file}...")
    elif line == "msx import all modules including .js .msx .py .jsx .tsx .json .ts":
        print("Importing all modules...")
    elif line == "msx rate":
        run_rate()
    elif line == "msx subscription check":
        check_subscription()
    elif line.startswith("msx subscribe"):
        parts = line.split()
        duration_hours = 24  # default
        if len(parts) > 2:
            try:
                duration_hours = int(parts[2])
                duration_hours = max(15, min(duration_hours, 72))
            except:
                pass
        subscribe(duration_hours)
    elif line == "msx restart":
        reset_extension_state()
    elif line == "msx create custom subscriptions manager":
        create_subscription_manager()
    else:
        print(f"Unknown MSX statement: {line}")


# ===============================
# Rating feature
# ===============================
def run_rate():
    print("Rate this extension (1-5):")
    rating = input("Enter your rating: ").strip()
    try:
        rating_int = int(rating)
        if 1 <= rating_int <= 5:
            print(f"Your rating of {rating_int} has been saved!")
            with open(RATINGS_FILE, "a", encoding="utf-8") as f:
                f.write(f"{rating_int}\n")
        else:
            print("Rating must be between 1 and 5")
    except:
        print("Invalid input. Rating not saved.")


# ===============================
# Subscription feature
# ===============================
def subscribe(duration_hours):
    start_timestamp = int(time.time())
    with open(SUBS_FILE, "w", encoding="utf-8") as f:
        f.write(f"duration_hours={duration_hours}\n")
        f.write(f"start_timestamp={start_timestamp}\n")
    print(f"Subscription activated for {duration_hours} hours!")


def check_subscription():
    if not os.path.exists(SUBS_FILE):
        print("No active subscription. Please subscribe to unlock this extension.")
        return False
    else:
        data = {}
        with open(SUBS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line:
                    key, val = line.strip().split("=")
                    data[key] = int(val)
        elapsed_hours = (time.time() - data.get("start_timestamp", 0)) / 3600
        if elapsed_hours > data.get("duration_hours", 0):
            print("Subscription expired! Restarting extension...")
            reset_extension_state()
            return False
        remaining = data.get("duration_hours", 0) - elapsed_hours
        print(f"Subscription active. {remaining:.2f} hours remaining.")
        return True


def reset_extension_state():
    print("Restarting extension and clearing subscription state...")
    if os.path.exists(SUBS_FILE):
        os.remove(SUBS_FILE)
    if os.path.exists(RATINGS_FILE):
        os.remove(RATINGS_FILE)
    print("Extension reset. You must start over.")


def create_subscription_manager():
    print("Creating custom subscription manager...")
    bot_code = """# subscription manager bot
function manage_subscriptions(user) {
    print "Checking subscription rules for $user..."
}
"""
    manager_file = "subscription_manager.msx"
    with open(manager_file, "w", encoding="utf-8") as f:
        f.write(bot_code)
    print(f"Subscription manager created: {manager_file}")


# ===============================
# Ghost commands
# ===============================
def run_ghost_commands(command_type):
    if not os.path.exists(GHOST_FILE):
        print("No ghost commands file found.")
        return
    with open(GHOST_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    if command_type in data:
        for key, action in data[command_type].items():
            print(f"Executing ghost command '{key}' -> {action}")
            if action == "restart.msx":
                reset_extension_state()


# ===============================
# Direct execution support
# ===============================
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python runner.py <path_to_msx_file>")
        sys.exit(1)
    msx_file = sys.argv[1]
    if not os.path.exists(msx_file):
        print(f"Error: File '{msx_file}' not found")
        sys.exit(1)
    run_msx_file(msx_file)
