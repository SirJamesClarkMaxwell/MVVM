import traceback
from viewmodels import ViewModel
from models.code_editor_model import CodeEditorModel
from data.code_editor_data import CodeEditorData,ScriptTab
from utils.logger import AppLogger

from imgui_bundle import imgui_color_text_edit,imgui

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


class CodeEditorViewModel(ViewModel):
    def __init__(self, model=None, data=None,app = None):
        super().__init__(model or CodeEditorModel(), data or CodeEditorData())
        self.editors: dict[str, (EditorUI,ScriptTab)] = {}

    def open_script(self, path: str,content:str):
        content = self.model.read_file(path)
        name = path.split("/")[-1]
        self.data.current_tab_name = name
        self.editors[name] = (EditorUI(content),ScriptTab(name, content))

