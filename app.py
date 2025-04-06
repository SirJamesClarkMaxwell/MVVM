from imgui_bundle import imgui, im_file_dialog, hello_imgui, immvision
from imgui_bundle.immapp import static

# import hello_imgui
from utils.logger import AppLogger
from utils.file_dialog import FileDialogController
from utils.thread_pool import Task, ThreadPool
from data import *
from models import *
from views import *
from viewmodels import *

import inspect, os


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
        AppLogger.get().info("Initializing App")

        self.setup_panels()
        self.create_dockable_windows()

        # ✅ Automatically load live_plot.py into DevTools
        self.initialize_app_state()
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
            CodeEditorPanel,
            CodeEditorViewModel,
            CodeEditorModel(),
            CodeEditorData(),
        )
        self.register_panel(
            "Terminal",
            TerminalPanel,
            TerminalViewModel,
            TerminalModel(),
            TerminalData(),
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
                AppLogger.get().info(f"Loaded CSV: {result.shape[0]} rows")

    def on_file_selected(self, path: str):
        try:
            with open(path, encoding="utf8") as f:
                content = f.read()
            editor_vm: CodeEditorViewModel = self.vm_store["DevTools"]
            editor_vm.open_script(path, content)
            AppLogger.get().info(f"📂 Opened in editor: {path}")
        except Exception as e:
            AppLogger.get().error(f"Failed to open {path}: {e}")

    def handle_shortcuts(self):
        io = imgui.get_io()

        self.last_shortcut_frame = getattr(self, "last_shortcut_frame", -1)

        if io.key_ctrl and imgui.is_key_pressed(imgui.Key.o, repeat=False):
            current_frame = imgui.get_frame_count()
            if current_frame != self.last_shortcut_frame:
                self.last_shortcut_frame = current_frame
                self.file_dialog.open()
                AppLogger.get().info("Ctrl+O pressed – opening file dialog")

    def create_dockable_windows(self):
        AppLogger.get().debug(f"{inspect.currentframe().f_code.co_name}")
        for label in self.panels.keys():
            self.add_dockable_window_for_panel(label)

        log_window = hello_imgui.DockableWindow()
        log_window.label = "Logs"
        log_window.dock_space_name = "MainDockSpace"
        log_window.gui_function = hello_imgui.log_gui
        self.dockable_windows.append(log_window)

        self.file_dialog = FileDialogController()
        self.file_dialog.result_callback = lambda path: self.on_file_selected(path)

    def add_dockable_window_for_panel(self, label):
        window = hello_imgui.DockableWindow()
        window.label = label
        window.dock_space_name = "MainDockSpace"
        window.gui_function = lambda label=label: self.render_panel(label)
        self.dockable_windows.append(window)

    def create_runner_params(self):
        AppLogger.get().debug(f"{inspect.currentframe().f_code.co_name}")

        params = hello_imgui.RunnerParams()
        params.app_window_params.window_title = "MVVM Paradise"
        params.imgui_window_params.enable_viewports = True
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
        vm = viewmodel_cls(model, view_data, self)
        panel = view_cls(vm)
        self.vm_store[name] = vm
        self.panels[name] = panel

    # def reload_script_panels(self):
    #     editor_vm: CodeEditorViewModel = self.vm_store["DevTools"]
    #     new_panels = editor_vm.reload_script_panels()

    #     self.update_script_panels(new_panels)  # 👈 Use the refactored method

    #     AppLogger.get().info(f"🔁 Script panels reloaded: {len(new_panels)} added")

    



    def initialize_app_state(self):
        try:
            editor_vm = self.vm_store.get("DevTools")  # or "CodeEditor" if renamed
            if editor_vm:
                path = os.path.join(
                    os.path.abspath(os.path.curdir), "Scripts", "live_plot.py"
                )
                if os.path.exists(path):
                    content = ""
                    with open(path, "r") as f:
                        content = f.read()
                    editor_vm.open_script(path, content)
                    AppLogger.get().info(f"📂 Loaded script: {path}")
                else:
                    AppLogger.get().warning(f"⚠️ Script not found: {path}")
        except Exception as e:
            AppLogger.get().error(f"❌ Failed to auto-load live_plot.py: {e}")
