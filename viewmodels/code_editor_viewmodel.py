import io, os, traceback,  contextlib

from imgui_bundle import imgui_color_text_edit,imgui

from utils.logger import AppLogger
from viewmodels import ViewModel
from models import Model,CodeEditorModel
from data import Data, CodeEditorData,ScriptTab


class EditorUI:
    def __init__(self, content: str):
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
    def set_content(self,content:str)->None:
        self.editor.set_text(content)

class CodeEditorViewModel(ViewModel):
    def __init__(self, model: Model, data: Data,app):
        super().__init__(model or CodeEditorModel(), data or CodeEditorData(),app)
        self.editors: dict[str, (EditorUI,ScriptTab)] = {}
        self.pending_closes = []  # queue of editor names pending confirmation
        self.confirming_close_name = None
        self.scope = {
            "app": app ,
            "vm_store": app.vm_store,
            "log": AppLogger.get(),}

    def open_script(self, path: str,content:str):
        content = self.model.read_file(path)
        AppLogger.get().debug(path)
        name = path.split("\\")[-1]
        self.data.current_tab_name = name
        self.editors[name] = (EditorUI(content),ScriptTab(name,content, path))

    def request_close_editor(self, name: str):
        tab = self.editors.get(name)
        if tab and tab.editor.is_dirty:
            self.confirming_close_name = name  # trigger confirmation popup
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
                # Optionally trigger "Save As" dialog here
                AppLogger.get().warn(f"⚠️ No file path for script '{name}'")

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




