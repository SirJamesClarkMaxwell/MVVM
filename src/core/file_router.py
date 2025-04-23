from pathlib import Path
from typing import List, Optional, Union,Callable
from core.logger import AppLogger



class FileRouter:
    def __init__(self, app) -> None:
        self.app = app
        self._file_path: Optional[Path] = None
        self._handlers: dict[str, Callable[[str], None]] = {}

        # Register default handlers
        self.register_handler(".txt", self._handle_text)
        self.register_handler(".py", self._handle_text)
        self.register_handler(".md", self._handle_text)
        self.register_handler(".png", self._handle_image)

    def register_handler(self, extension: str, handler: Callable[[str], None]):
            self._handlers[extension.lower()] = handler

    def route(self, filepath: str):
        path = Path(filepath)
        ext = path.suffix.lower()

        handler = self._handlers.get(ext)
        if handler:
            handler(filepath)
        else:
            self._handle_unknown(filepath)

    def _handle_text(self, filepath: str):
        from app import App  # or inject this later
        editor_vm = App.get().vm_store["CodeEditor"]
        editor_vm.load_file(filepath)

    def _handle_image(self, filepath: str):
        print(f"[Image Viewer Placeholder] Open image: {filepath}")

    def _handle_unknown(self, filepath: str):
        print(f"[Unhandled File] No handler for: {filepath}")