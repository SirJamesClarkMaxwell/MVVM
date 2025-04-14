from typing import Callable, Dict, List

from .shortcut_context import ShortcutContext
from .shortcut_registry import ShortcutRegistry


class ShortcutManager:
    def __init__(self, registry: ShortcutRegistry, context_service: ShortcutContext):
        self.registry = registry
        self.context_service = context_service
        self.target_map: Dict[str, Callable] = {}

    def bind_viewmodel_targets(self, mapping: Dict[str, Callable]):
        self.target_map = mapping

    def handle_key_event(self, keys: List[str]):
        context = self.context_service.get_active_context()
        shortcut = self.registry.get_by_keys_and_context(keys, context)
        if shortcut:
            target_fn = self.target_map.get(shortcut.target)
            if target_fn:
                try:
                    target_fn()
                except Exception as e:
                    print(f"Shortcut '{shortcut.id}' failed: {e}")

