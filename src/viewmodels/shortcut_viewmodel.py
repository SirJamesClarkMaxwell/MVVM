import os
from typing import List,Optional,Dict,Tuple

from numpy import short

from core.logger import AppLogger
from core.shortcuts.shortcut import Shortcut,ShortcutBinding
from core.shortcuts import ShortcutManager,ShortcutRegistry,ShortcutContext


class ShortcutViewModel:

    def __init__(self,app, config_path: str = "code/config/shortcuts.json"):
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
        # TODO: test bind_shortcut function
        binging_conditions,messege = self._check_binding_conditions(bingings=bindings, shortcut=to_bind)

        def check_conditions(binding: ShortcutBinding, shortcut: Shortcut) -> bool:
            shocrtcut_id, binding_id = shortcut.id,binding.id
            return binding_id == shocrtcut_id
        if binging_conditions:
            AppLogger.get().info(messege)
            for shortcut, binding in zip(to_bind, bindings):
                if not check_conditions(binding, shortcut):
                    AppLogger.get().error(f"Binding conditions are not met for {binding.id} and {shortcut.id}")
                    continue
                shortcut.bingings = binding
                self.shortcut_registry.register(shortcut)
                self.shortcut_manager.register(binding)

        else:
            AppLogger.get().error(messege)
            return None

    def _check_binding_conditions(self, **kwargs) -> Tuple[bool,str]:
        # TODO: test _check_binding_conditions
        bingings = kwargs["bingings"]
        shortcut = kwargs["shortcut"]
        list_condition = isinstance(bingings, list) and isinstance(shortcut, list)
        individual_condition = isinstance(bingings, ShortcutBinding) and isinstance(shortcut, Shortcut)

        if list_condition or individual_condition:
            if not list_condition and  individual_condition:
                return (False, "Binding conditions are not met, list expected")
            if not individual_condition and not list_condition:
                return (False, "Binding conditions are not met, individual expected")
            if len(bingings) != len(shortcut):
                return (False, "Binding conditions are not met, length mismatch")

            return (True, "Binding conditions are met")

    def handle_shortcut(self, shortcuts: List[Shortcut]):
        self.shortcut_manager.handle_key_event(shortcuts, self.shortcut_registry)

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
        #TODO : test load_from_file function
        if not os.path.exists(path):
            AppLogger.get().error(f"There are no file or directory: {path}")
            return None
        try:
            return ShortcutManager.load_from_file(path)
        except OSError as e:
            AppLogger.get().error(f"[ShortcutViewModel] Import failed: {e}")
            return None

    def export_shortcuts(self, path: str)->None:
        #TODO : test export_shortcuts function
        try:
            ShortcutManager.save_to_file(path, self.shortcut_registry.list_all())
        except OSError as e:
            AppLogger.get().error(f"[ShortcutViewModel] Export failed: {e}")

    def reset_to_defaults(self)->None:
        defaults = ShortcutManager.get_defaults()
        self.shortcut_registry.replace_all(defaults)
        self.shortcuts = defaults
        ShortcutManager.save_to_file(self.config_path, defaults)
