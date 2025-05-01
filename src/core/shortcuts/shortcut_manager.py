from typing import Callable, Dict, List, Any
import json
from dataclasses import asdict
from src.core.logger import AppLogger
from src.core.shortcuts.shortcut import Shortcut, ShortcutBinding
from src.core.shortcuts.shortcut_context import ShortcutContext
from src.core.shortcuts.shortcut_registry import ShortcutRegistry


class ShortcutManager:
    def __init__(self, context_service: ShortcutContext):
        self.context_service = context_service

    def handle_key_event(
        self, keys: List[str], registry: ShortcutRegistry, app: Any
    ) -> None:
        context = self.context_service.get_active_context()
        shortcut = registry.get_by_keys_and_context(keys, context)
        if not shortcut:
            return
        try:
            if shortcut.enable_threading:
                app.thread_pool.submit(shortcut.id,shortcut.__call__,app)
            else:
                shortcut(app)
        except ValueError as e:
            AppLogger.get().error(f"Shortcut '{shortcut.id}' failed: {e}")


    @staticmethod
    def load_from_file(filepath: str) -> list[Shortcut]:
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)

        for item in data:
            item.setdefault("enable_threading", False)

            # Ensure context is always a list
            if isinstance(item.get("context"), str):
                item["context"] = [item["context"]]

            # Optional: same for category if needed
            if isinstance(item.get("category"), list):
                item["category"] = ", ".join(item["category"])

        return [Shortcut(**item) for item in data]

    @staticmethod
    def save_to_file(filepath: str, shortcuts: list[Shortcut]) -> None:
        AppLogger.get().info(
            f"\
            ShortcutModel.save_to_file: saving shortcuts to file: {filepath}"
        )
        with open(filepath, "w", encoding="utf8") as file:
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
                enable_threading=True
            ),
            # Add more defaults as needed
        ]

    def register(self, binding: ShortcutBinding) -> None:
        AppLogger.get().info(f"Registering binding: {binding.id}")
        # Add logic to register the binding if necessary
        pass
