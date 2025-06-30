from click import help_option
from imgui_bundle import hello_imgui, imgui
import traceback

def main():
    # Sample state variables for the demo
    feature_x_enabled = False
    some_slider_value = 50
    log_messages = [
        "Program started",
        "User logged in",
        "Temperature set to 22°C",
        "Error: cannot connect to server",
    ]

    # GUI callback for the "Logs" panel
    def gui_logs():
        if imgui.begin("gui Logs"):
            imgui.text_unformatted("Application Log:")
            imgui.separator()
            for msg in log_messages:
                imgui.bullet_text(msg)
            imgui.end()
    # GUI callback for the "Settings" panel
    def gui_settings():
        if imgui.begin("Gui settings"):
            nonlocal feature_x_enabled, some_slider_value
            _, feature_x_enabled = imgui.checkbox("Enable Feature X", feature_x_enabled)
            _, some_slider_value = imgui.slider_int("Volume", some_slider_value, 0, 100)
            imgui.text(f"Feature X is {'enabled' if feature_x_enabled else 'disabled'}.")
            imgui.end()

    # Configure main application window and docking parameters
    runner_params = hello_imgui.RunnerParams()
    runner_params.app_window_params.window_title = "Docking Example"
    # runner_params.app_window_params.window_size = (800, 600)
    # runner_params.app_window_params.window_size_auto = False
    runner_params.app_window_params.restore_previous_geometry = (
        True  # restore last window size/pos
    )

    # Enable full-screen dock space and viewports via ImGui config
    runner_params.imgui_window_params.show_menu_bar = (
        True  # Show menu bar (with "View" menu, etc.)
    )
    runner_params.imgui_window_params.enable_viewports = (
        True  # Allow panels to be dragged out as native windows
    )
    runner_params.imgui_window_params.default_imgui_window_type = (
        hello_imgui.DefaultImGuiWindowType.provide_full_screen_dock_space
    )

    # Define two dockable panels and assign them to the main dock space
    logs_window = hello_imgui.DockableWindow()
    logs_window.label = "Logs"
    logs_window.dock_space_name = "MainDockSpace"
    logs_window.gui_function = gui_logs

    settings_window = hello_imgui.DockableWindow()
    settings_window.label = "Settings"
    settings_window.dock_space_name = "MainDockSpace"
    settings_window.gui_function = gui_settings

    runner_params.docking_params.dockable_windows = [logs_window]#, settings_window]
    # (No initial docking_splits specified – both windows will dock into MainDockSpace as tabs)

    # Run the application using the manual render loop
    hello_imgui.manual_render.setup_from_runner_params(runner_params)
    while not hello_imgui.get_runner_params().app_shall_exit:
        hello_imgui.manual_render.render()
        
    hello_imgui.manual_render.tear_down()


if __name__ == "__main__":
    main()
