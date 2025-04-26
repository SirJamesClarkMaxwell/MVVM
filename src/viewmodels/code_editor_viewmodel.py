import io, os, traceback, contextlib
from typing import cast

from imgui_bundle import imgui_color_text_edit, imgui

from src.core.logger import AppLogger

from src.models.code_editor_model import CodeEditorModel
from src.data.code_editor_data import  CodeEditorData, ScriptTab
from src.views.runtime_panel import RuntimePanel


class EditorUI:
    def __init__(self, content: str,*args,**kwargs):
        TextEditor = imgui_color_text_edit.TextEditor
        self.editor = TextEditor()
        self.editor.set_language_definition(TextEditor.LanguageDefinition.python())
        self.editor.set_show_whitespaces(False)
        self.editor.set_tab_size(4)
        self.editor.set_text(content)

    def update_model(self) -> str:
        return self.editor.get_text()

    def render(self, label: str, size):
        self.editor.render("ScriptEditor", a_size=imgui.get_content_region_avail())

    def set_content(self, content: str) -> None:
        self.editor.set_text(content)


class CodeEditorViewModel:
    def __init__(self, app):
        self.model =  CodeEditorModel()
        self.data =  CodeEditorData()
        
        self.editors: dict[str, tuple[EditorUI, ScriptTab]] = {}
        self.pending_closes = []  # queue of editor names pending confirmation
        self.confirming_close_name = None
        self.scope = {
            "app": app,
            "vm_store": app.vm_store,
            "log": AppLogger.get(),
        }
        self.runtime_panels: dict[str, RuntimePanel] = {}

    def open_script(self, path: str):
        content = self.model.read_file(path)
        AppLogger.get().debug(path)
        name = path.split("\\")[-1]
        self.data.current_tab_name = name
        self.editors[name] = (EditorUI(content), ScriptTab(name, content, path))

    def request_close_editor(self, name: str):
        if name in self.editors:
            editor, tab = self.editors[name]
            if tab.is_dirty:
                self.confirming_close_name = name
            else:
                self.force_close_editor(name)

    def force_close_editor(self, name: str):
        if name in self.editors:
            del self.editors[name]

    def save_script(self, name: str):
        if name in self.editors:
            editor, tab = self.editors[name]
            if tab.filepath:
                self.model.save_file(tab.filepath, tab.content)
                tab.is_dirty = False
            else:
                AppLogger.get().warning(f"⚠️ No file path for script '{name}'")

    def run_current_script(self):
        name = self.data.current_tab_name
        if name in self.editors:
            editor, tab = self.editors[name]

            buffer = io.StringIO()
            local_scope = self.scope.copy()

            with contextlib.redirect_stdout(buffer), contextlib.redirect_stderr(buffer):
                try:
                    exec(tab.content, local_scope)
                    tab.output = buffer.getvalue()
                    tab.output += "\nScript executed successfully."
                except Exception:
                    error_output = traceback.format_exc()
                    tab.output = buffer.getvalue() + "\n" + error_output
                    AppLogger.get().error(f"Script error in {name}:\n{error_output}")

    def reload_current_script(self):
        name = self.data.current_tab_name
        if name in self.editors:
            editor, tab = self.editors[name]
            if tab.filepath and os.path.exists(tab.filepath):
                new_content = self.model.read_file(tab.filepath)
                tab.content = new_content
                editor.set_content(new_content)
                tab.is_dirty = False
                AppLogger.get().info(f"Reloaded: {tab.filepath}")

    def clear_output(self):
        name = self.data.current_tab_name
        if name in self.editors:
            _, tab = self.editors[name]
            tab.output = ""
            AppLogger.get().debug(f"Cleared output for {name}")

    def extract_dynamic_panels(self):
        dynamic_panels = []

        for name, (editor, tab) in self.editors.items():
            local_scope = self.scope.copy()

            try:
                exec(tab.content, local_scope)

                panel_title = local_scope.get("panel_title", name)
                render_fn = local_scope.get("render", None)

                if callable(render_fn):
                    dynamic_panels.append((panel_title, render_fn))

            except Exception as e:
                AppLogger.get().error(f"[Script Error] '{name}': {e}")

        return dynamic_panels

    def update_script_panels(self, new_panels: dict[str, RuntimePanel]):
        for key in list(self.runtime_panels):
            if key.startswith("script:"):
                del self.runtime_panels[key]
        self.runtime_panels.update(new_panels)
        AppLogger.get().info(f"🧪 Registered {len(new_panels)} runtime script panels")

    def reload_script_panels(self):
        dynamic_panels = {}
        for name, (editor, tab) in self.editors.items():
            local_scope = self.scope.copy()
            try:
                exec(tab.content, local_scope)
                panel_title = local_scope.get("panel_title", name)
                render_fn = local_scope.get("render", None)
                if callable(render_fn):
                    dynamic_panels[f"script:{panel_title}"] = RuntimePanel(
                        panel_title, render_fn
                    )
            except Exception as e:
                AppLogger.get().error(f"❌ Script panel '{name}' failed to load: {e}")
        self.runtime_panels = dynamic_panels
