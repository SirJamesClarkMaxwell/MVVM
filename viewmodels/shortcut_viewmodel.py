import os
from typing import List

from core.logger import AppLogger
from core.shortcuts.shortcut import Shortcut
from core.shortcuts import ShortcutManager,ShortcutRegistry,ShortcutContext


class ShortcutViewModel:
    def __init__(self,app, config_path: str = "config/shortcuts.json",*args,**kwargs):
        self.shortcut_manager = ShortcutManager(ShortcutContext())
        self.shortcut_registry = ShortcutRegistry()
        self.config_path = config_path
        self._pending_changes: List[Shortcut] = []
        AppLogger.get().info(f"Initialized Shortcut ViewModel")
        AppLogger.get().info(f"Loaded shortcuts from {config_path}")

    def get_shortcuts_by_category(self) -> dict[str, List[Shortcut]]:
        categorized = {}
        for sc in self.shortcut_registry.list_all():
            categorized.setdefault(sc.category, []).append(sc)
        return categorized

    def update_shortcut(self, updated: Shortcut) -> bool:
        # Check for conflicts
        conflicts = self.shortcut_registry.find_conflicts(updated)
        if conflicts:
            AppLogger.get().info(
                f"[ShortcutViewModel] Conflict detected for: {updated.keys} in {updated.context}")
            return False

        # Replace in local list
        self.shortcuts = [
            updated if sc.id == updated.id else sc
            for sc in self.shortcuts
        ]
        self._pending_changes = self.shortcuts.copy()
        return True

    def commit_changes(self):
        self.shortcut_registry.replace_all(self._pending_changes)
        ShortcutManager.save_to_file(self.config_path, self._pending_changes)

    def load_from_file(self, path: str) -> bool:
        if not os.path.exists(path):
            AppLogger.get().error(f"There are no file or directory: {path}")
            return False
        try:
            shortcuts = ShortcutManager.load_from_file(path)
            self.shortcut_registry.replace_all(shortcuts)
            
            return True
        except Exception as e:
            AppLogger.get().error(f"[ShortcutViewModel] Import failed: {e}")
            return False

    def export_shortcuts(self, path: str)->None:
        try:
            ShortcutManager.save_to_file(path, self.shortcut_registry.list_all())
        except Exception as e:
            AppLogger.get().error(f"[ShortcutViewModel] Export failed: {e}")

    def reset_to_defaults(self)->None:
        defaults = ShortcutManager.get_defaults()
        self.shortcut_registry.replace_all(defaults)
        self.shortcuts = defaults
        ShortcutManager.save_to_file(self.config_path, defaults)
        
    def handle_shortcut(self,shortcuts:List[Shortcut]):
        self.shortcut_manager.handle_key_event(shortcuts,self.shortcut_registry)