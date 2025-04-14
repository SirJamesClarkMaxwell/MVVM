import os
from typing import List

from core.shortcuts.shortcut import Shortcut
from core.shortcuts.shortcut_registry import ShortcutRegistry
from models.shortcut_model import ShortcutModel


class ShortcutViewModel:
    def __init__(self, config_path: str = "config/shortcuts.json"):
        self.registry = ShortcutRegistry()
        self.config_path = config_path
        self.shortcuts: List[Shortcut] = self.registry.list_all()
        self._pending_changes: List[Shortcut] = []

    def get_shortcuts_by_category(self) -> dict[str, List[Shortcut]]:
        categorized = {}
        for sc in self.shortcuts:
            categorized.setdefault(sc.category, []).append(sc)
        return categorized

    def update_shortcut(self, updated: Shortcut) -> bool:
        # Check for conflicts
        conflicts = self.registry.find_conflicts(updated)
        if conflicts:
            print(
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
        self.registry.replace_all(self._pending_changes)
        ShortcutModel.save_to_file(self.config_path, self._pending_changes)

    def import_shortcuts(self, path: str) -> bool:
        if not os.path.exists(path):
            return False
        try:
            shortcuts = ShortcutModel.load_from_file(path)
            self.registry.replace_all(shortcuts)
            self.shortcuts = shortcuts
            # persist to main config
            ShortcutModel.save_to_file(self.config_path, shortcuts)
            return True
        except Exception as e:
            print(f"[ShortcutViewModel] Import failed: {e}")
            return False

    def export_shortcuts(self, path: str):
        try:
            ShortcutModel.save_to_file(path, self.registry.list_all())
        except Exception as e:
            print(f"[ShortcutViewModel] Export failed: {e}")

    def reset_to_defaults(self):
        defaults = ShortcutModel.get_defaults()
        self.registry.replace_all(defaults)
        self.shortcuts = defaults
        ShortcutModel.save_to_file(self.config_path, defaults)
        ShortcutModel.save_to_file(self.config_path, defaults)
        ShortcutModel.save_to_file(self.config_path, defaults)
