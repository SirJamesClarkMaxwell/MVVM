

from dataclasses import asdict, dataclass
import json

from core.shortcuts.shortcut import Shortcut


@dataclass
class ShortcutModel:
    @staticmethod    
    def load_from_file(filepath: str) -> list[Shortcut]:
        with open(filepath, "r") as file:
            data = json.load(file)
        return [Shortcut(**item) for item in data]


    @staticmethod    
    def save_to_file(filepath: str, shortcuts: list[Shortcut]):
        with open(filepath, "w") as file:
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
                target="file_panel_viewmodel.open_file",
            ),
            # Add more defaults as needed
        ]
