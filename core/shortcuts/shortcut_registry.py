
from typing import List, Optional

from .shortcut import Shortcut


class ShortcutRegistry:
    def __init__(self) -> None:
        self._shortcuts: List[Shortcut] = []

    def register(self, shortcut: Shortcut):
        self._shortcuts.append(shortcut)

    def unregister(self, shortcut_id: str):
        self._shortcuts = [s for s in self._shortcuts if s.id != shortcut_id]

    def list_all(self) -> List[Shortcut]:
        return self._shortcuts

    def find_conflicts(self, new_shortcut: Shortcut) -> List[Shortcut]:
        return [
            s
            for s in self._shortcuts
            if set(s.keys) == set(new_shortcut.keys)
            and any(ctx in s.context for ctx in new_shortcut.context)
            and s.id != new_shortcut.id
        ]

    def get_by_keys_and_context(
        self, keys: List[str], context: str
    ) -> Optional[Shortcut]:
        for item in self._shortcuts:
            if set(item.keys) == set(keys) and (
                context in item.context or "Global" in item.context
            ):
                return item
        return None

    def replace_all(self, new_shortcuts: List[Shortcut]):
        self._shortcuts = new_shortcuts


