from typing import Callable, Dict, List
import json 
from dataclasses import asdict
from core.logger import AppLogger
from .shortcut import Shortcut
from .shortcut_context import ShortcutContext
from .shortcut_registry import ShortcutRegistry


class ShortcutManager:
    def __init__(self, context_service: ShortcutContext):
        
        self.context_service = context_service
        self.target_map: Dict[str, Callable] = {}

    def bind_viewmodel_targets(self, mapping: Dict[str, Callable]):
        self.target_map = mapping

    def handle_key_event(self, keys: List[str],registry:ShortcutRegistry):
        context = self.context_service.get_active_context()
        shortcut = registry.get_by_keys_and_context(keys, context)
        if not shortcut:
            # AppLogger.get().warning("ShortcutManager.handle_key_event")
            return
        target_fn = self.target_map.get(shortcut.target)
        if not target_fn:
            return 
        try:
            target_fn()
        except Exception as e:
            AppLogger.get().error(f"Shortcut '{shortcut.id}' failed: {e}")

    @staticmethod    
    def load_from_file(filepath: str) -> list[Shortcut]:
        AppLogger.get().info(f"\
            ShortcutModel.load_from_file: Loading shortcuts from file: {filepath}")
        with open(filepath, "r") as file:
            data = json.load(file)
        return [Shortcut(**item) for item in data]


    @staticmethod    
    def save_to_file(filepath: str, shortcuts: list[Shortcut]):
        AppLogger.get().info(f"\
            ShortcutModel.save_to_file: saving shortcuts to file: {filepath}")
        with open(filepath, "w") as file:
            json.dump([asdict(s) for s in shortcuts], file, indent=4)


    @staticmethod    
    def get_defaults() -> list[Shortcut]:
        return [
            Shortcut(
                id="open_file",
                keys=["Ctrl+O"],
                category="File Operations",
                context=["Global"],
                description="Open a file",
                target="file_panel_viewmodel.open_file",
            ),
            # Add more defaults as needed
        ]