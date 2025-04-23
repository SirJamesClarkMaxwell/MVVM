from core.shortcuts.shortcut_registry import ShortcutRegistry
from core.shortcuts.shortcut_context import ShortcutContext
from core.shortcuts.shortcut_manager import ShortcutManager

class AppSettings:
    def __init__(self):
        self._shortcuts_path = "config/shortcuts.json"
        self.shortcut_context = ShortcutContext()
        self.shortcut_registry = ShortcutRegistry()


    @property
    def shortcut_path(self):
        return self._shortcuts_path