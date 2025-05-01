import os
from time import sleep
from types import NoneType
from typing import Any, Callable, List

from src.core.shortcuts.shortcut import Shortcut, ShortcutBinding
from src.core.logger import AppLogger

# * Global shortcuts
def create_global_shortcut_bindings(app:Any) -> list[ShortcutBinding]:

    bindigs = []

    def get_project_path(app: Any) -> str:
        return app.project_path

    def open_file(app: Any, file_path: str) -> None:
        handle = app.file_dialog.open_files(file_path)
        while  len(app.file_dialog.paths_to_route) is  0:
            sleep(0.1)
        return app.file_dialog.paths_to_route

    def print_file_path(app: Any, file_path: str) -> None:
        for path in app.file_dialog.paths_to_route:
            app.file_dialog.route_path(path)
            AppLogger.get().info(
                f"Printing file path from: shortcut_bindings.print_file_path: {path}"
            )

    def print_folder_content(app: Any, directory_path: str) -> None:
        AppLogger.get().info(f"Directory path: {directory_path}")
        for item in os.listdir(directory_path):
            AppLogger.get().info(f"Item: {item}")

    open_file_obj = ShortcutBinding(
        "open_file",
        pre_process=get_project_path,
        function=open_file,
        post_process=print_file_path,
    )

    save_file = ShortcutBinding(
        "save_file",
        pre_process=get_project_path,
        function=app.file_dialog.save_file,
        post_process=print_file_path,
    )

    open_directory = ShortcutBinding(
        "open_directory",
        pre_process=get_project_path,
        function=app.file_dialog.open_folder,
        post_process=print_folder_content,
    )

    return bindigs + [open_file_obj
    ,save_file,open_directory]
