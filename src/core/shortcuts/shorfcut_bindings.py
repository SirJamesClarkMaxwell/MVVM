from typing import Any, Callable, List

from .shortcut import Shortcut, ShortcutBinding


# * Global shortcuts
def create_global_shortcut_bindings(app:Any) -> list[ShortcutBinding]:
    
    bindigs = []


    open_file = ShortcutBinding("open_file"
                        ,function=app.file_dialog.open,
                        pre_process=app.file_dialog.get_file_path,
                        post_process=app.file_dialog.open_file)

