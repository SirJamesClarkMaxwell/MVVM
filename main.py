
from app import App
from imgui_bundle import hello_imgui

def main():
    app = App()
    runner_params = app.initialize()
    runner_params.imgui_window_params.default_imgui_window_type = \
    hello_imgui.DefaultImGuiWindowType.provide_full_screen_dock_space
    hello_imgui.run(runner_params)

if __name__ == "__main__":
    main()
