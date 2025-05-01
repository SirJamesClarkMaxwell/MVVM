import os
from time import sleep
from types import NoneType
from typing import Any, Callable, List

from src.core.shortcuts.shortcut import Shortcut, ShortcutBinding
from src.core.logger import AppLogger


class App:
    ...

# * Global shortcuts
def create_global_shortcut_bindings(app:App) -> list[ShortcutBinding]:

    bindigs = []

    def get_project_path(app: App) -> str:
        return app.project_path

    def register_opening_file(app: App) -> None:
        project_path = get_project_path(app)
        app.file_dialog.open_files(project_path)

    def open_file(app: App, file_path: str) -> None:
        while  len(app.file_dialog.paths_to_route) is  0:
            sleep(0.1)
        for path in app.file_dialog.paths_to_route:
            app.file_dialog.route_path(path)
            AppLogger.get().info(
                f"Printing file path from: shortcut_bindings.open_file: {path}"
            )
        app.file_dialog.paths_to_route = []
        return None

    def print_file_path(app: App, file_path: str) -> None:
        AppLogger.get().info(
            f"Printing file path from: shortcut_bindings.open_file: {file_path}"
        )
        return None

    def print_folder_content(app: App, directory_path: str) -> None:
        AppLogger.get().info(f"Directory path: {directory_path}")
        for item in os.listdir(directory_path):
            AppLogger.get().info(f"Item: {item}")

    def save_project(app: App) -> None:
        AppLogger.get().error(
            "Functionality of saving Project has not been implemented yet!"
        )
        raise NotImplementedError("This functionality has not been implemented yet!")

    open_file_obj = ShortcutBinding(
        "open_file",
        pre_process=register_opening_file,
        function=open_file,
        post_process=print_file_path,
    )

    save_project_obj = ShortcutBinding(
        "save_project",
        pre_process=get_project_path,
        function=save_project,
        post_process=print_file_path,
    )

    open_directory = ShortcutBinding(
        "open_directory",
        pre_process=get_project_path,
        function=app.file_dialog.open_folder,
        post_process=print_folder_content,
    )

    return bindigs + [open_file_obj, save_project_obj, open_directory]
