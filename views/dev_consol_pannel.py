from imgui_bundle import imgui,imgui_ctx
from views import Panel
from utils.logger import AppLogger

class ScriptsPanel(Panel):
    def __init__(self, view_model):
        super().__init__(view_model)

    def render(self):
        # with imgui_ctx.begin("DevTools"):
        avail_x,avail_y = imgui.get_content_region_avail()
        imgui.dock_space(imgui.get_id("ScriptsDock"), imgui.ImVec2(avail_x,avail_y/2))
        if imgui.begin("Quick Console", True):
            changed, self.view_model.data.code = imgui.input_text_multiline(
                "Quick Console###code_input",
                self.view_model.data.code,
                imgui.ImVec2(-1, -1)
            )
            imgui.end()
        if imgui.begin("Script Dock", True):  # window that contains tab bar
            changed, self.view_model.data.editor_content = imgui.input_text_multiline(
                "Script Window###editor_input",
                self.view_model.data.editor_content,
                imgui.ImVec2(-1, -1)
            )
            imgui.end()
            
        for script in self.view_model.data.script_list:
            selected = (script == self.view_model.data.selected_script)
            clicked, _ = imgui.selectable(script, selected, imgui.SelectableFlags_.allow_double_click)
            if clicked:
                AppLogger.get().debug(f"{script=} has been clicked")
                self.view_model.data.selected_script = script
            if selected and imgui.is_item_hovered() and imgui.is_mouse_double_clicked(0):
                self.view_model.load_script(script)
                AppLogger.get().debug(f"{script=} double-clicked, loaded.")
            if selected and clicked:
                self.view_model.data.selected_script = script
                self.view_model.load_script(script)
                AppLogger.get().debug(f"{self.view_model.data.selected_script=}")
                AppLogger.get().debug(f"{self.view_model.data.code=}")

        if imgui.button("Refresh List"):
            self.view_model.refresh_script_list()
            AppLogger.get().debug("Refresh List button has been clicked")
        imgui.same_line()
        
        if imgui.button("Run Code"):
            self.view_model.run_console_code()
            AppLogger.get().debug("Run Code button has been clicked")
        imgui.same_line()
            
        if imgui.button("Run Script") and self.view_model.data.code is not "":
            self.view_model.run_editor_script()
            AppLogger.get().debug("Run Code button has been clicked")
            
        imgui.separator()
        
        imgui.text("Output")
        imgui.begin_child("ConsoleOutput", size=imgui.ImVec2(0, 150), child_flags=imgui.ChildFlags_.borders)
        imgui.text_wrapped(self.view_model.data.output_log or self.view_model.data.exec_result)
        imgui.end_child()
