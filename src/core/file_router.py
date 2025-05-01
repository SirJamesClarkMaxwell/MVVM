from pathlib import Path
from typing import  Optional, Callable
from src.core.logger import AppLogger


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

    def register_handler(self, extension: str, handler: Callable[[str], None])-> None:
        self._handlers[extension.lower()] = handler
        AppLogger.get().info(f"Registered handler for {extension} files.")

    def route(self, filepath: str)->None:
        path = Path(filepath)
        ext = path.suffix.lower()
        handler = self._handlers.get(ext)
        if handler:
            try:
                handler(filepath)
            except NotImplementedError:
                AppLogger.get().error(f"Handler for {ext} files is not implemented.")
        else:
            self._handle_unknown(filepath)


    def route_folder(self, folder_path: str) -> None:
        pass
        #self.print_folder_content(folder_path)  # <-- This prints folder content


    def _handle_text(self, filepath: str)->None:
        editor_vm = self.app.vm_store["DevTools"]
        editor_vm.open_script(filepath)
        AppLogger.get().info(f"Opened Text file of: {filepath}")

    def _handle_image(self, filepath: str) -> None:
        # TODO: Implement folder routing logic
        AppLogger.get().info(f"[Image Viewer Placeholder] Open image: {filepath}")
        raise NotImplementedError("Folder routing is not implemented yet.")

    def _handle_unknown(self, filepath: str) -> None:
        AppLogger.get().warning(f"[Unhandled File] No handler for: {filepath}")
