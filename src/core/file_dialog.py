import os
from typing import Dict
from imgui_bundle import portable_file_dialogs as pfd
from src.core.file_router import FileRouter


HandleType = pfd.open_file| pfd.select_folder| pfd.save_file
class FileDialogController:

    def __init__(self, app):
        self._hangles:Dict[str,HandleType] = {
            "open_file_handle": None,
            "open_folder_handle": None  ,
            "save_file_handle": None,
        }
        self.file_router = FileRouter(app)
        self.app = app
        self.paths_to_route = []

    def open_files(self, default_path: str) -> None:
        title: str = "Select File"
        file_options: pfd.opt = pfd.opt.multiselect

        self._hangles["open_file_handle"] = pfd.open_file(
            title=title, default_path=default_path, options=file_options
        )

    def open_folder(self, default_path: str):
        title = "Select Folder"
        directory_options: pfd.opt = pfd.opt.multiselect
        self._hangles["open_folder_handle"] = pfd.select_folder(
            title=title,
            default_path=default_path,
            options=directory_options,
        )

    def save_file(self, title="Save File", default_path="", filters=None):
        if filters is None:
            filters = ["*.*"]
        self._hangles["save_file_handle"] = pfd.save_file(title, default_path, filters=filters)


    def render(self):
        for handle_name, handle in self._hangles.items():
            if handle and handle.ready() and handle.result():
                result = handle.result()
                self.paths_to_route = [*result] if isinstance(result ,list) else [result]
                self._hangles[handle_name] = None


    def route_path(self, path: str):
        if os.path.isdir(path):
            self.file_router.route_folder(path)  # <-- Will now call print_folder_content!
        else:
            self.file_router.route(path)
