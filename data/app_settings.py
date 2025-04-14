from core.shortcuts.shortcut_registry import ShortcutRegistry
from core.shortcuts.shortcut_context import ShortcutContext
from core.shortcuts.shortcut_manager import ShortcutManager
from models.shortcut_model import ShortcutModel

class AppSettings:
    def __init__(self):
        self._shortcuts_path = "config/shortcuts.json"
        self.shortcut_context = ShortcutContext()
        self.shortcut_registry = ShortcutRegistry()

        try:
            shortcuts = ShortcutModel.load_from_file(self._shortcuts_path)
        except Exception:
            shortcuts = ShortcutModel.get_defaults()

        self.shortcut_registry.replace_all(shortcuts)
        self.shortcut_manager = ShortcutManager(
            self.shortcut_registry,
            self.shortcut_context
        )

    @property
    def shortcut_path(self):
        return self._shortcuts_path