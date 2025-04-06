import os
from utils.logger import AppLogger

class CodeEditorModel:
    def __init__(self, script_dir="Scripts"):
        self.script_dir = script_dir
        if not os.path.exists(self.script_dir):
            os.makedirs(self.script_dir)

    def read_file(self, path: str) -> str:
        with open(path, encoding="utf-8") as f:
            return f.read()

    def save_file(self, path: str, content: str):
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
            
            
    def list_scripts(self):
        return [f for f in os.listdir(self.script_dir) if f.endswith(".py")]

    def load_script(self, name):
        path = os.path.join(self.script_dir, name)
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def run_code(self, code, scope):
        exec(code, scope)
