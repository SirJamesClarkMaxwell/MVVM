from abc import ABC, abstractmethod
from typing import Any
from imgui_bundle import hello_imgui

class Panel(ABC):
    """Base class for UI panels."""

    def __init__(self, view_model,name:str):
        self.view_model = view_model
        self.__window:hello_imgui.DockableWindow = hello_imgui.DockableWindow()
        self.__setup_widnow(name)

    def __setup_widnow(self,name:str):
        # self.__window.call_begin_end = False
        self.__window.dock_space_name = "MainDockSpace"
        self.__window.gui_function = self.render
        self.__window.label = name

    # def set_renderer_function(self,name:str, )
    @property
    def window(self):
        return self.__window
    @property
    def app(self)->Any:
        return self.view_model.app
    @property
    def visible(self) -> bool:
        if self.__window is not None:
            return self.__window.is_visible
        return False

    @visible.setter
    def visible(self, value: bool):
        if self.__window is not None:
            self.__window.is_visible = value

    def __bool__(self):
        return self.__window.is_visible
    
    @abstractmethod
    def render(self):
        """Render the panel's UI."""
        pass
