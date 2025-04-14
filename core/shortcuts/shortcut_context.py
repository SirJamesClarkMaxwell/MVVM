class ShortcutContext:
    def __init__(self):
        self._active_context: str = "Global"

    def get_active_context(self) -> str:
        return self._active_context

    def set_active_context(self, context: str):
        self._active_context = context
