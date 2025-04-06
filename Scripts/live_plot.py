from imgui_bundle import imgui

panel_title = "Test Panel"

def render():
    if imgui.begin(panel_title):
        imgui.text("Hello from script!")
        imgui.end()
