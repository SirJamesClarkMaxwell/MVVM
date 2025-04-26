from typing import Any, Callable, List

from src.core.shortcuts.shortcut import Shortcut, ShortcutBinding
from src.core.logger import AppLogger

# * Global shortcuts
def create_global_shortcut_bindings(app:Any) -> list[ShortcutBinding]:

    bindigs = []

    def get_project_path(app: Any) -> str:
        return app.project_path
    def print_file_path(app: Any, file_path: str) -> None:
        AppLogger.get().info(f"File path: {file_path}")

    open_file = ShortcutBinding(
        "open_file",
        pre_process=get_project_path,
        function=app.file_dialog.open_files,
        post_process=print_file_path,
    )
    return bindigs + [open_file]
