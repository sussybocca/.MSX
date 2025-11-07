# mini_interpreter.py
import os
import json
import shutil

class MiniInterpreter:
    def __init__(self):
        self.mode = "local"  # "local" or "web"
        self.repeat = False
        self.recombine = False
        self.ton = 50
        self.code_max = 1000
        self.react_enabled = False
        self.exe_enabled = False
        self.web_enabled = False
        self.code_size_range = (55, 1000)
        self.error_log = []

    # ----------------------
    # Mode selection
    # ----------------------
    def choose_mode(self, mode):
        if mode == ".mini":
            self.mode = "local"
        elif mode == ".minitron":
            self.mode = "web"
        else:
            self._log_error(102, "Invalid mode")
        print(f"[INFO] Mode set to {self.mode}")

    # ----------------------
    # File commands
    # ----------------------
    def read_file(self, file_path):
        if not os.path.exists(file_path):
            self._log_error(101, f"File {file_path} not found")
            return None
        with open(file_path, "r") as f:
            content = f.read()
        print(f"[INFO] Read file: {file_path}")
        return content

    def execute_file(self, file_path):
        content = self.read_file(file_path)
        if content is None:
            return
        print(f"[EXECUTE] Running {file_path}...\n{content}")

    def compile_file(self, file_path):
        print(f"[COMPILE] Compiling {file_path} for mode: {self.mode}")
        # In a real implementation, compile logic goes here

    # ----------------------
    # Build / Package
    # ----------------------
    def build(self, output_name):
        if self.mode == "local":
            self._build_local(output_name)
        elif self.mode == "web":
            self._build_web(output_name)

    def _build_local(self, output_name):
        folder_name = output_name + "_local"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        # Copy all .mini files to build folder
        for file in os.listdir("."):
            if file.endswith(".mini"):
                shutil.copy(file, folder_name)
        print(f"[BUILD] Local build completed: {folder_name}")

    def _build_web(self, output_name):
        file_name = output_name + ".minitron"
        # Combine all .mini files into one for web
        with open(file_name, "w") as outfile:
            for file in os.listdir("."):
                if file.endswith(".mini"):
                    with open(file, "r") as f:
                        outfile.write(f"# From {file}\n")
                        outfile.write(f.read() + "\n\n")
        print(f"[BUILD] Web build completed: {file_name}")

    # ----------------------
    # Settings
    # ----------------------
    def set_repeat(self, value: bool):
        self.repeat = value
        print(f"[INFO] Repeat set to {self.repeat}")

    def set_recombine(self, value: bool):
        self.recombine = value
        print(f"[INFO] Recombine set to {self.recombine}")

    def change_ton(self, value: int):
        self.ton = value
        print(f"[INFO] Ton set to {self.ton}")

    def set_code_max(self, value: int):
        self.code_max = value
        print(f"[INFO] Max code size set to {self.code_max}")

    def reset_code(self, value: int):
        self.code_max = value
        print(f"[INFO] Code reset to {self.code_max}")

    def enable_feature(self, feature: str, value: bool):
        if feature == "react":
            self.react_enabled = value
        elif feature == "exe":
            self.exe_enabled = value
        elif feature == "web":
            self.web_enabled = value
        print(f"[INFO] Feature {feature} set to {value}")

    def set_code_range(self, min_val: int, max_val: int):
        self.code_size_range = (min_val, max_val)
        print(f"[INFO] Code range set to {self.code_size_range}")

    # ----------------------
    # Error handling
    # ----------------------
    def _log_error(self, code, message):
        self.error_log.append({"code": code, "message": message})
        print(f"[ERROR {code}] {message}")

    def show_errors(self):
        for err in self.error_log:
            print(f"Error {err['code']}: {err['message']}")

    # ----------------------
    # Interactive command loop
    # ----------------------
    def run_command(self, cmd_line):
        parts = cmd_line.strip().split()
        if not parts:
            return
        cmd = parts[0].lower()
        args = parts[1:]
        if cmd == "read" and args:
            self.read_file(args[0])
        elif cmd == "execute" and args:
            self.execute_file(args[0])
        elif cmd == "compile" and args:
            self.compile_file(args[0])
        elif cmd == "build" and args:
            self.build(args[0])
        elif cmd == "set_repeat" and args:
            self.set_repeat(args[0].lower() == "true")
        elif cmd == "set_recombine" and args:
            self.set_recombine(args[0].lower() == "true")
        elif cmd == "change_ton" and args:
            self.change_ton(int(args[0]))
        elif cmd == "set_code_max" and args:
            self.set_code_max(int(args[0]))
        elif cmd == "enable_feature" and len(args) == 2:
            self.enable_feature(args[0], args[1].lower() == "true")
        elif cmd == "show_errors":
            self.show_errors()
        else:
            self._log_error(102, f"Unknown command: {cmd_line}")

# ----------------------
# Example usage / Interactive CLI
# ----------------------
if __name__ == "__main__":
    mini = MiniInterpreter()
    mini.choose_mode(".mini")

    print("Welcome to MiniInterpreter CLI. Type 'exit' to quit.")
    while True:
        cmd = input(".mini> ")
        if cmd.lower() == "exit":
            break
        mini.run_command(cmd)
