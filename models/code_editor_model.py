import os

from core.logger import AppLogger


class CodeEditorModel:
    def __init__(self, script_dir="Scripts"):
        self.script_dir = script_dir
        AppLogger.get().debug(
            f"Initializing CodeEditorModel with script_dir='{script_dir}'"
        )
        if not os.path.exists(self.script_dir):
            os.makedirs(self.script_dir)
            AppLogger.get().info(
                f"Created script directory: {self.script_dir}")

    def read_file(self, path: str) -> str:
        AppLogger.get().info(f"Reading file: {path}")
        try:
            with open(path, encoding="utf-8") as f:
                content = f.read()
            AppLogger.get().debug(
                f"Successfully read file: {path} ({len(content)} bytes)"
            )
            return content
        except Exception as e:
            AppLogger.get().error(f"Failed to read file '{path}': {e}")
            raise

    def save_file(self, path: str, content: str):
        AppLogger.get().info(f"Saving file: {path}")
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            AppLogger.get().debug(f"Saved file: {path} ({len(content)} bytes)")
        except Exception as e:
            AppLogger.get().error(f"Failed to save file '{path}': {e}")
            raise

    def list_scripts(self):
        AppLogger.get().debug(f"Listing scripts in: {self.script_dir}")
        try:
            scripts = [f for f in os.listdir(
                self.script_dir) if f.endswith(".py")]
            AppLogger.get().info(f"Found {len(scripts)} script(s)")
            return scripts
        except Exception as e:
            AppLogger.get().error(f"Error listing scripts: {e}")
            return []

    def load_script(self, name):
        path = os.path.join(self.script_dir, name)
        AppLogger.get().info(f"Loading script: {name} → {path}")
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            AppLogger.get().debug(
                f"Loaded script '{name}' ({len(content)} bytes)")
            return content
        except Exception as e:
            AppLogger.get().error(f"Failed to load script '{name}': {e}")
            raise

    def run_code(self, code, scope):
        AppLogger.get().info("Running code in scope")
        try:
            exec(code, scope)
            AppLogger.get().debug("Code executed successfully")
        except Exception as e:
            AppLogger.get().error(f"Error executing code: {e}")
            raise
            raise
