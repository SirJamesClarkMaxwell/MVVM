import os
import traceback
from imgui_bundle import imgui
from views import Panel
from viewmodels import ViewModel
from utils.logger import AppLogger

class DevToolsPanel(Panel):
    def __init__(self, view_model):
        super().__init__(view_model)
        self.script_dir = "scripts"
        self.script_list = []
        self.selected_script = None
        self.editor_content = ""
        self.output_log = ""
        self.code = ""
        self.exec_result = ""
        # ✅ No App import here! Use injected app from view_model
        self.scope = {
            "app": view_model.app,
            "vm_store": view_model.app.vm_store,
            "imgui": imgui,
            "print": self._capture_output
        }

        self.refresh_script_list()

    def _capture_output(self, *args):
        self.output_log += " ".join(str(a) for a in args) + "\n"

    def refresh_script_list(self):
        if os.path.exists(self.script_dir):
            self.script_list = [f for f in os.listdir(self.script_dir) if f.endswith(".py")]
        else:
            os.makedirs(self.script_dir)
            self.script_list = []

    def render(self):
        changed, self.code = imgui.input_text_multiline(
            "##console_input", self.code, imgui.ImVec2(500, 200)
        )
        if imgui.button("Run Code"):
            self.exec_result = ""
            try:
                exec(self.code, self.scope)
            except Exception as e:
                AppLogger.get().debug(self.output_log)
                self.output_log = traceback.format_exc()

        imgui.separator()
        # imgui.text("Output:")
        # imgui.begin_child("ConsoleOutput", ize=imgui.ImVec2(0, 100), child_flags=imgui.ChildFlags_.borders)
        # imgui.text_wrapped(self.exec_result)
        # imgui.end_child()
        
        imgui.begin_child("ScriptList", size=imgui.ImVec2(0, 200), child_flags=imgui.ChildFlags_.borders)
        imgui.text("Scripts")
        for script in self.script_list:
            if imgui.selectable(script, script == self.selected_script):
                self.selected_script = script
                with open(os.path.join(self.script_dir, script), "r", encoding="utf-8") as f:
                    self.editor_content = f.read()
        if imgui.button("Refresh List"):
            self.refresh_script_list()
        imgui.end_child()

        imgui.same_line()

        imgui.begin_group()
        imgui.text(f"Editing: {self.selected_script or 'None'}")
        changed, self.editor_content = imgui.input_text_multiline(
            "##ScriptEditor", self.editor_content, imgui.ImVec2(500, 300)
        )

        if imgui.button("Run Script") and self.selected_script:
            self.output_log = ""
            try:
                exec(self.editor_content, self.scope)
            except Exception:
                self.output_log = traceback.format_exc()

        imgui.separator()
        imgui.text("Output")
        imgui.begin_child("ConsoleOutput", size=imgui.ImVec2(0, 150), child_flags=imgui.ChildFlags_.borders)
        imgui.text_wrapped(self.exec_result)
        imgui.end_child()
        imgui.end_group()
