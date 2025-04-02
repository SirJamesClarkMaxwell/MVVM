from imgui_bundle import imgui
from views import Panel
# from ..app import App
import traceback


class DevConsolePanel(Panel):
    def __init__(self, view_model):
        super().__init__(view_model)
        self.code = ""
        self.exec_result = ""

        self.scope = {
            "app": view_model.app,
            "imgui": imgui,
            "vm_store": view_model.app.vm_store,
            "panels": view_model.app.panels,
            "print": self._capture_output
        }

    def _capture_output(self, *args):
        self.exec_result += " ".join(str(a) for a in args) + "\n"

    def render(self):
        changed, self.code = imgui.input_text_multiline(
            "##console_input", self.code, imgui.ImVec2(500, 200)
        )

        if imgui.button("Run Code"):
            self.exec_result = ""
            try:
                exec(self.code, self.scope)
            except Exception as e:
                self.exec_result = traceback.format_exc()

        imgui.separator()
        imgui.text("Output:")
        imgui.begin_child("ConsoleOutput", size=imgui.ImVec2(0, 100),child_flags=imgui.ChildFlags_.borders)
        imgui.text_wrapped(self.exec_result)
        imgui.end_child()
