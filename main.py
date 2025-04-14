
from app import App
from imgui_bundle import hello_imgui,imgui

def main():
    print(type(imgui.Key.a))
    print(imgui.get_key_name(imgui.Key.a))
    print(type(imgui.Key(546)))
    print(imgui.get_key_name(imgui.Key(546)))
    
    app = App()
    runner_params = app.initialize()
    runner_params.imgui_window_params.default_imgui_window_type = \
    hello_imgui.DefaultImGuiWindowType.provide_full_screen_dock_space
    hello_imgui.run(runner_params)

if __name__ == "__main__":
    main()
