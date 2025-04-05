from imgui_bundle import imgui, imgui_ctx, imgui_color_text_edit
from views import Panel
from utils.logger import AppLogger


class CodeEditorPanel(Panel):
    def __init__(self, view_model):
        super().__init__(view_model)

    def render(self):
        avail_x, avail_y = imgui.get_content_region_avail()
        if imgui.begin_table("CodeEditorLayout", 1, imgui.TableFlags_.no_borders_in_body):
            # === Row 0: Dockable editor space ===
            imgui.table_next_row()
            imgui.table_set_column_index(0)
            imgui.dock_space(imgui.get_id("EditorDockspace"), imgui.ImVec2(avail_x, avail_y * 0.75))
            self.render_code_space()
            
            imgui.table_next_row()
            imgui.table_set_column_index(0)
            # if imgui.button("Run"):
            #     self.view_model.run_current_script()
            # imgui.same_line()
            # if imgui.button("Save"):
            #     self.view_model.save_current_script()
            imgui.separator()
            imgui.text("Output:")
            with imgui_ctx.begin_child("EditorOutput", imgui.ImVec2(-1,100),imgui.ChildFlags_.borders):
                if self.view_model.editors.get(self.view_model.data.current_tab_name):
                    (current_editor,current_tab) = self.view_model.editors[self.view_model.data.current_tab_name]
                    imgui.text_wrapped(current_tab.output or "No output yet.")
                # imgui_ctx.end_child()
            imgui.end_table()

    def render_code_space(self):
        for name,(editor,tab) in self.view_model.editors.items():
            if imgui.begin(name, True):
                
                self.view_model.data.current_tab_name = name
                imgui.text(f"Editing: {name}")
                editor.render("ScriptEditor", imgui.get_content_region_avail())
                        # Push changes back to the data model
                new_content = editor.update_model()
                        
                if new_content != tab.content:
                    tab.content = new_content
                    tab.is_dirty = True
            imgui.end()
        


