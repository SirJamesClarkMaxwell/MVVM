from imgui_bundle import imgui
from imgui_bundle import hello_imgui
from views import Panel

ALL_THEMES = [
    hello_imgui.ImGuiTheme_.darcula_darker,
    hello_imgui.ImGuiTheme_.darcula,
    hello_imgui.ImGuiTheme_.imgui_colors_classic,
    hello_imgui.ImGuiTheme_.imgui_colors_dark,
    hello_imgui.ImGuiTheme_.imgui_colors_light,
    hello_imgui.ImGuiTheme_.material_flat,
    hello_imgui.ImGuiTheme_.photoshop_style,
    hello_imgui.ImGuiTheme_.gray_variations,
    hello_imgui.ImGuiTheme_.gray_variations_darker,
    hello_imgui.ImGuiTheme_.microsoft_style,
    hello_imgui.ImGuiTheme_.cherry,
    hello_imgui.ImGuiTheme_.light_rounded,
    hello_imgui.ImGuiTheme_.so_dark_accent_blue,
    hello_imgui.ImGuiTheme_.so_dark_accent_yellow,
    hello_imgui.ImGuiTheme_.so_dark_accent_red,
    hello_imgui.ImGuiTheme_.black_is_black,
    hello_imgui.ImGuiTheme_.white_is_white,
]

ALL_THEMES_NAMES = [theme.name for theme in ALL_THEMES]

class SettingsPanel(Panel):
    def __init__(self, view_model):
        super().__init__(view_model)
        self.font_size = 1.4  # Default global scale for font size
        self.preview_font_size = self.font_size
        self.current_theme_idx = ALL_THEMES_NAMES.index("photoshop_style")
        self.initialized = False

    def render(self):
        if not self.initialized:
            self.initialized = True
            hello_imgui.apply_theme(ALL_THEMES[self.current_theme_idx])
            imgui.get_io().font_global_scale = self.font_size
            imgui.get_io().font_global_scale = self.preview_font_size
        imgui.text("Settings Panel")
        imgui.separator()

        # === Style Editor Section ===
        if imgui.tree_node("Style Editor"):
            imgui.show_style_editor()
            imgui.tree_pop()

        # === Font Size Section ===
        if imgui.tree_node("Font Size"):
            imgui.text("Font Size")
            changed, self.preview_font_size = imgui.slider_float("##FontSize", self.preview_font_size, 0.5, 2.0, "%.1f")
            if changed:
                imgui.get_io().font_global_scale = self.preview_font_size
            imgui.tree_pop()

        # === Theme Section ===
        if imgui.tree_node("Theme"):
            imgui.text("Select Theme")
            changed, self.current_theme_idx = imgui.list_box(
                "##Theme", self.current_theme_idx, ALL_THEMES_NAMES, len(ALL_THEMES_NAMES)
            )
            if changed:
                hello_imgui.apply_theme(ALL_THEMES[self.current_theme_idx])
            imgui.tree_pop()
