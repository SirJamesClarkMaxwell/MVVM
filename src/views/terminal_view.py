from imgui_bundle import imgui,imgui_ctx
from views import Panel

class TerminalPanel(Panel):
    def __init__(self, view_model):
        super().__init__(view_model)

    def render(self):
        avail = imgui.get_content_region_avail()
        terminal_heigh = avail.y -30
        with imgui_ctx.begin_child("TerminalOutput", size=imgui.ImVec2(-1, terminal_heigh), child_flags=0):
            imgui.text_wrapped(self.view_model.data.terminal_output)
            if self.view_model.data.auto_scroll:
                imgui.set_scroll_here_y(1.0)

        # Command input
        # if imgui.is_window_focused():
        #     imgui.set_keyboard_focus_here()
        changed, self.view_model.data.terminal_input = imgui.input_text(
            ">>>###TerminalInput",
            self.view_model.data.terminal_input,
            0 | imgui.InputTextFlags_.enter_returns_true.value if hasattr(imgui.InputTextFlags_.enter_returns_true, 'value') else 0
        )

        if changed and self.view_model.data.terminal_input.strip():
            self.view_model.run_command()
