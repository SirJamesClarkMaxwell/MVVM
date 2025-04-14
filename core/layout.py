from Code.views.calculator_panel import CalculatorPanel
from imgui_bundle import hello_imgui


def create_docking(app_state):
    calculator_panel = CalculatorPanel(app_state.calculator_vm)

    calc_window = hello_imgui.DockableWindow()
    calc_window.label = "Calculator"
    calc_window.dock_space_name = "MainDockSpace"
    calc_window.gui_function = calculator_panel.render

    logs_window = hello_imgui.DockableWindow()
    logs_window.label = "Logs"
    logs_window.dock_space_name = "MiscSpace"
    logs_window.gui_function = hello_imgui.log_gui  # Built-in!

    return [calc_window, logs_window]
