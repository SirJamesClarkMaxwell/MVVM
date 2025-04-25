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
    def __init__(self, view_model, shortcut_viewmodel):
        super().__init__(view_model)
        self.shortcut_viewmodel = shortcut_viewmodel
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
        if imgui.tree_node("Shortcut Settings"):
            shortcut_vm = self.shortcut_viewmodel
            self.draw_shortcut_settings_panel(shortcut_vm)
            imgui.tree_pop()

    def draw_shortcut_settings_panel(self,shortcut_vm):


        if imgui.button("Save Changes"):
            shortcut_vm.commit_changes()
        imgui.same_line()
        if imgui.button("Import"):
            # Ideally open file dialog here
            shortcut_vm.import_shortcuts("config/imported_shortcuts.json")
        imgui.same_line()
        if imgui.button("Export"):
            shortcut_vm.export_shortcuts("config/exported_shortcuts.json")
        imgui.same_line()
        if imgui.button("Reset to Defaults"):
            shortcut_vm.reset_to_defaults()

        imgui.separator()

        categorized = shortcut_vm.get_shortcuts_by_category()

        for category, shortcuts in categorized.items():
            # FIXME: Fix problem with tree node, shortcuts per category should be in one tree node 
            if imgui.collapsing_header(category, flags=imgui.TreeNodeFlags_.default_open):
                if imgui.begin_table(f"Table_{category}", 3,imgui.TableFlags_.borders|imgui.TableFlags_.row_bg|imgui.TableFlags_.resizable):#, imgui.TABLE_BORDERS | imgui.TABLE_ROW_BACKGROUND):
                    imgui.table_setup_column("Action")
                    imgui.table_setup_column("Shortcut Keys")
                    imgui.table_setup_column("Description")
                    imgui.table_headers_row()

                    for sc in shortcuts:
                        imgui.table_next_row()
                        imgui.table_set_column_index(0)
                        imgui.text(sc.id)

                        imgui.table_set_column_index(1)
                        key_input = f"##{sc.id}"
                        changed, new_keys = imgui.input_text(key_input, ", ".join(sc.keys), 64)
                        if changed:
                            updated = sc.__class__(**{
                                **sc.__dict__,
                                "keys": [k.strip() for k in new_keys.split(",")]
                            })
                            success = shortcut_vm.update_shortcut(updated)
                            if not success:
                                imgui.push_style_color(imgui.COLOR_TEXT, 1.0, 0.4, 0.4)
                                imgui.text("⚠ Conflict!")
                                imgui.pop_style_color()

                        imgui.table_set_column_index(2)
                        imgui.text(sc.description)

                    imgui.end_table()

