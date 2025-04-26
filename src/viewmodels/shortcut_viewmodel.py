import os
import types
from typing import List,Optional,Dict,Tuple

from numpy import short

from src.core.logger import AppLogger
from src.core.shortcuts import Shortcut, ShortcutBinding
from src.core.shortcuts import ShortcutManager, ShortcutRegistry, ShortcutContext


class ShortcutViewModel:

    def __init__(self,app, config_path: str = "src/config/shortcuts.json"):
        self.shortcut_manager = ShortcutManager(ShortcutContext())
        self.shortcut_registry = ShortcutRegistry()
        self.config_path = config_path
        self._pending_changes: List[Shortcut] = []
        self.shortcuts: List[Shortcut] = []
        self.shortcuts = ShortcutManager.load_from_file(config_path)
        self.app = app
        AppLogger.get().info("Initialized Shortcut ViewModel")
        AppLogger.get().info(f"Loaded shortcuts from {config_path}")

    def bind_shortcut(self,to_bind:List[Shortcut]|Shortcut,bindings:List[ShortcutBinding]|ShortcutBinding) -> None:
        binging_conditions,messege = self._check_binding_conditions(bingings=bindings, shortcut=to_bind)

        if not binging_conditions:
            AppLogger.get().error(messege)
            return None

        AppLogger.get().info(messege)

        if isinstance(to_bind, Shortcut) and isinstance(bindings, ShortcutBinding):
            to_bind = [to_bind]
            bindings = [bindings]

        for shortcut, binding in zip(to_bind, bindings):
            if shortcut.id != binding.id:
                AppLogger.get().error(f"Binding conditions are not met for {binding.id} and {shortcut.id}")
                shortcut.bingings = None
                continue
            shortcut.bingings = binding
            self.shortcut_registry.register(shortcut)
            self.shortcut_manager.register(binding)

    def _check_binding_conditions(self, **kwargs) -> Tuple[bool, str]:
        bindings = kwargs["bingings"]
        shortcut = kwargs["shortcut"]

        list_condition = isinstance(bindings, list) and isinstance(shortcut, list)
        individual_condition = isinstance(bindings, ShortcutBinding) and isinstance(
            shortcut, Shortcut
        )

        if list_condition:
            # List mode
            if not all(isinstance(b, ShortcutBinding) for b in bindings):
                return (
                    False,
                    "Binding conditions are not met, bindings list has invalid types",
                )
            if not all(isinstance(s, Shortcut) for s in shortcut):
                return (
                    False,
                    "Binding conditions are not met, shortcuts list has invalid types",
                )
            if len(bindings) != len(shortcut):
                return (False, "Binding conditions are not met, length mismatch")
            return (True, "Binding conditions are met")

        elif individual_condition:
            return (True, "Binding conditions are met")

        else:
            return (
                False,
                "Binding conditions are not met, expected either both lists or both single objects",
            )

    def handle_shortcut(self, shortcuts: List[Shortcut]):
        self.shortcut_manager.handle_key_event(shortcuts, self.shortcut_registry,self.app)

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

    def load_from_file(self, path: str) -> Optional[Shortcut]:
        # TODO : test load_from_file function
        if not os.path.exists(path):
            AppLogger.get().error(f"There are no file or directory: {path}")
            return None
        try:
            return ShortcutManager.load_from_file(path)
        except OSError as e:
            AppLogger.get().error(f"[ShortcutViewModel] Import failed: {e}")
            return None

    def export_shortcuts(self, path: str) -> None:
        try:
            if not os.path.isdir(os.path.dirname(path)):
                raise OSError(f"Invalid directory: {os.path.dirname(path)}")
            ShortcutManager.save_to_file(path, self.shortcut_registry.list_all())
        except OSError as e:
            AppLogger.get().error(f"[ShortcutViewModel] Export failed: {e}")
            raise

    def reset_to_defaults(self)->None:
        defaults = ShortcutManager.get_defaults()
        self.shortcut_registry.replace_all(defaults)
        self.shortcuts = defaults
        ShortcutManager.save_to_file(self.config_path, defaults)
