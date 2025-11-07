# mini_interpreter.py
import os
import json

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
        # Simulate execution
        print(f"[EXECUTE] Running {file_path}...\n{content}")

    def compile_file(self, file_path):
        print(f"[COMPILE] Compiling {file_path} for mode: {self.mode}")
        # Placeholder for compile logic

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
# Example usage
# ----------------------
if __name__ == "__main__":
    mini = MiniInterpreter()
    mini.choose_mode(".mini")
    mini.read_file("example.mini")
    mini.execute_file("example.mini")
    mini.set_repeat(True)
    mini.set_recombine(True)
    mini.change_ton(55)
    mini.set_code_max(55)
    mini.enable_feature("react", True)
    mini.show_errors()
