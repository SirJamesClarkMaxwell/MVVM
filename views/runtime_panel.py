from typing import Callable
from utils.logger import AppLogger
from imgui_bundle import imgui


class RuntimePanel:
    def __init__(self, title: str, render_func:Callable):
        self.title = title
        self.render_func = render_func

    def render(self):
        try:
            imgui.begin(self.title)
            self.render_func()
            imgui.end()
        except Exception as e:
            imgui.begin(self.title)
            AppLogger.get().error(f"❌ Error: {e}")
            imgui.end()
