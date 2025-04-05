from imgui_bundle import hello_imgui, imgui, im_file_dialog
from utils.logger import AppLogger
from utils.file_dialog import FileDialogController
from utils.thread_pool import Task, ThreadPool

from data import *
from models import *
from views import *
from viewmodels import *

import inspect


class App:
    _instance = None

    @classmethod
    def get(cls):
        if not cls._instance:
            cls._instance = App()
        return cls._instance

    def __init__(self):
        self.panels = {}
        self.dockable_windows = []
        self.vm_store = {}  # optional: {"calculator": vm, ...}
        self.thread_pool = ThreadPool()
        self.application_data = ApplicationData()

    def initialize(self):
        AppLogger.get().info("🚀 Initializing App")

        self.setup_panels()
        self.create_dockable_windows()

        runner_params = self.create_runner_params()
        runner_params.docking_params.dockable_windows = self.dockable_windows
        return runner_params

    def setup_panels(self):
        AppLogger.get().debug(f"{inspect.currentframe().f_code.co_name}")
        self.register_panel(
            "Calculator",
            CalculatorPanel,
            CalculatorViewModel,
            CalculatorModel(),
            CalculatorData(),
        )
        self.register_panel(
            "DevTools",
            ScriptsPanel,
            lambda m, d: CodeEditorViewModel(m, d, app=self),
        )
        self.register_panel(
            "Terminal", TerminalPanel, lambda model, data: TerminalViewModel(app=self)
        )

    def render_panel(self, name):
        self.handle_shortcuts()
        self.file_dialog.render()
        for label, panel in self.panels.items():
            if label == name:
                panel.render()
                break
        completed_tasks = self.thread_pool.get_completed()
        for task in completed_tasks:
            result = task.result()
            if result is not None:
                AppLogger.get().info(f"✅ Loaded CSV: {result.shape[0]} rows")

    def on_file_selected(self, path: str):
        model = self.vm_store["Calculator"].model
        task = self.thread_pool.submit("Load CSV", model.load_csv, path)
        self.pending_model_task = task
        AppLogger.get().info(f"📂 Selected: {path}")

    def handle_shortcuts(self):
        io = imgui.get_io()
        ctrl_pressed = io.key_ctrl
        # AppLogger.get().debug(
        #     f"{inspect.currentframe().f_code.co_name}: ctrl {"Pressed" if ctrl_pressed else "Not Pressed"}"
        # )
        if ctrl_pressed and imgui.is_key_pressed(imgui.Key.o, repeat=False):
            AppLogger.get().info("Ctrl+O pressed – opening file dialog")
            self.file_dialog.open()

    def create_dockable_windows(self):
        AppLogger.get().debug(f"{inspect.currentframe().f_code.co_name}")
        for label, _ in self.panels.items():
            window = hello_imgui.DockableWindow()
            window.label = label
            window.dock_space_name = "MainDockSpace"
            window.gui_function = lambda label=label: self.render_panel(label)
            self.dockable_windows.append(window)

        log_window = hello_imgui.DockableWindow()
        log_window.label = "Logs"
        log_window.dock_space_name = "MainDockSpace"
        log_window.gui_function = hello_imgui.log_gui
        self.dockable_windows.append(log_window)

        self.file_dialog = FileDialogController()
        self.file_dialog.result_callback = lambda path: self.on_file_selected(path)

    def create_runner_params(self):
        AppLogger.get().debug(f"{inspect.currentframe().f_code.co_name}")
        params = hello_imgui.RunnerParams()
        params.app_window_params.window_title = "MVVM Paradise"
        params.imgui_window_params.enable_viewports = True
        # params.imgui_window_params.enable_docking = True
        params.imgui_window_params.default_imgui_window_type = (
            hello_imgui.DefaultImGuiWindowType.provide_full_screen_dock_space
        )
        return params

    def register_panel(
        self,
        name: str,
        view_cls,
        viewmodel_cls,
        model: Model = None,
        view_data: Data = None,
    ):
        AppLogger.get().debug(f"{inspect.currentframe().f_code.co_name}")
        vm = viewmodel_cls(model, view_data)
        panel = view_cls(vm)
        self.vm_store[name] = vm
        self.panels[name] = panel
