from imgui_bundle import imgui, imgui_ctx, imgui_color_text_edit
from views import Panel
from utils.logger import AppLogger


class ScriptsPanel(Panel):
    def __init__(self, view_model):
        super().__init__(view_model)
        self.editor = self.create_editor()
    def render(self):
        # with imgui_ctx.begin("DevTools"):
        avail_x, avail_y = imgui.get_content_region_avail()
        imgui.dock_space(
            imgui.get_id("ScriptsDock"), imgui.ImVec2(avail_x, avail_y / 2)
        )
        if imgui.begin("Script Dock", True):
            if self.view_model.data.editor_content != self.editor.get_text():
                self.editor.set_text(self.view_model.data.editor_content)
            self.editor.render("ScriptEditor",False, imgui.ImVec2(imgui.get_content_region_avail()))

            # Save updated code back to the data model
            self.view_model.data.editor_content = self.editor.get_text()
            imgui.end()

        for script in self.view_model.data.script_list:
            selected = script == self.view_model.data.selected_script
            clicked, _ = imgui.selectable(
                script, selected, imgui.SelectableFlags_.allow_double_click
            )
            if clicked:
                AppLogger.get().debug(f"{script=} has been clicked")
                self.view_model.data.selected_script = script
            if (
                selected
                and imgui.is_item_hovered()
                and imgui.is_mouse_double_clicked(0)
            ):
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
        imgui.begin_child(
            "ConsoleOutput",
            size=imgui.ImVec2(0, 150),
            child_flags=imgui.ChildFlags_.borders,
        )
        imgui.text_wrapped(
            self.view_model.data.output_log or self.view_model.data.exec_result
        )
        imgui.end_child()

    def create_editor(self):
        from imgui_bundle import imgui, imgui_color_text_edit as ed, imgui_md
        TextEditor = ed.TextEditor
        ed = imgui_color_text_edit.TextEditor()
        ed.set_language_definition(TextEditor.LanguageDefinition.python())
        ed.set_show_whitespaces(False)
        ed.set_tab_size(4)
        return ed
