from typing import Any, Callable, List

from .shortcut import Shortcut, ShortcutBinding


# * Global shortcuts
def create_global_shortcut_bindings(app:Any) -> list[ShortcutBinding]:

    bindigs = []

    def get_project_path(app: Any) -> str:
        return tuple(app.project_path)
    open_file = ShortcutBinding("open_file",
                        pre_process=app.file_dialog.get_file_path,
                        function=app.file_dialog.open,
                        post_process=app.file_dialog.open_file)
