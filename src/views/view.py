from abc import ABC, abstractmethod
from typing import Any

class Panel(ABC):
    """Base class for UI panels."""

    def __init__(self, view_model):
        self.view_model = view_model
        self.render_panel = True

    @property
    def app(self)->Any:
        return self.view_model.app

    @abstractmethod
    def render(self):
        """Render the panel's UI."""
        pass
