from abc import ABC, abstractmethod


class Panel(ABC):
    """Base class for UI panels."""

    def __init__(self, view_model):
        self.view_model = view_model

    @abstractmethod
    def render(self):
        """Render the panel's UI."""
        pass
