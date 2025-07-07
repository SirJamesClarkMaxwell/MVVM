import os,sys
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

    def register_opening_file(app: Any) -> None:
        project_path = get_project_path(app)
        app.file_dialog.open_files(project_path)

    def open_file(app: Any, file_path: str) -> None:
        while  len(app.file_dialog.paths_to_route) is  0:
            sleep(0.1)
        for path in app.file_dialog.paths_to_route:
            app.file_dialog.route_path(path)
            AppLogger.get().info(
                f"Printing file path from: shortcut_bindings.open_file: {path}"
            )
        app.file_dialog.paths_to_route = []
        return None

    def print_file_path(app: Any, file_path: str) -> None:
        AppLogger.get().info(
            f"Printing file path from: shortcut_bindings.open_file: {file_path}"
        )
        return None

    def print_folder_content(app: Any, directory_path: str) -> None:
        AppLogger.get().info(f"Directory path: {directory_path}")
        for item in os.listdir(directory_path):
            AppLogger.get().info(f"Item: {item}")

    def save_project(app: Any) -> None:
        AppLogger.get().error(
            "Functionality of saving Project has not been implemented yet!"
        )
        return None
        # raise NotImplementedError("This functionality has not been implemented yet!")
    def exit_app(app,*args,**kwargs):
        app.running = False

    open_file_obj = ShortcutBinding(
        "Open File",
        pre_process=register_opening_file,
        function=open_file,
        post_process=print_file_path,
    )

    save_project_obj = ShortcutBinding(
        "Save Project",
        pre_process=get_project_path,
        function=save_project,
        post_process=print_file_path,
    )

    open_directory = ShortcutBinding(
        "Open Directory",
        pre_process=get_project_path,
        function=app.file_dialog.open_folder,
        post_process=print_folder_content,
    )
    shutdown_app = ShortcutBinding(
        "App Shutdown",
        pre_process=save_project,
        function= exit_app,
        post_process=lambda app, *args,**kwargs: None
        
    )

    return bindigs + [open_file_obj, save_project_obj, open_directory,shutdown_app]
def create_dev_tool_shortcut_binding(app:Any)->list[ShortcutBinding]:
    bindigs = []

    def reload_active_script(app: Any, *args, **kwargs) -> None:
        AppLogger.get().debug(f"Reloading {app.vm_store["DevTools"].script_to_run}")
        app.vm_store["DevTools"].reload_current_script()

    def run_currect_script(app: Any, *args, **kwargs) -> None:
        AppLogger.get().debug(f"Running {app.vm_store["DevTools"].script_to_run}")
        app.vm_store["DevTools"].reload_script_panels()

    run_active_script_obj = ShortcutBinding(
        "Run Script", pre_process=None, function=run_currect_script, post_process=None
    )
    reload_active_script_obj = ShortcutBinding(
        "Reload Script",
        pre_process=None,
        function=reload_active_script,
        post_process=None,
    )
    reload_and_run_active_script_obj = ShortcutBinding(
        "Reload and Run Script",
        pre_process=reload_active_script,
        function=run_currect_script,
        post_process=None,
    )
    return bindigs + [
        run_active_script_obj,
        reload_active_script_obj,
        reload_and_run_active_script_obj,
    ]
