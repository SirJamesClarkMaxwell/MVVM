from imgui_bundle import imgui, im_file_dialog, hello_imgui, immvision
from imgui_bundle.immapp import static

# import hello_imgui
from core.logger import AppLogger
from core.file_dialog import FileDialogController
from core.thread_pool import Task, ThreadPool
from data import *
from models import *
from views import *
from viewmodels import *

import inspect, os

from views.settings_panel import SettingsPanel


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
        AppLogger.get().debug(f"Setting up panels")
        self.register_panel(
            "Calculator",
            CalculatorPanel,
            CalculatorViewModel
            
        )
        self.register_panel(
            "DevTools",
            CodeEditorPanel,
            CodeEditorViewModel
        )
        self.register_panel(
            "Terminal",
            TerminalPanel,
            TerminalViewModel
        )
        self.register_panel(
            "Settings",
            SettingsPanel,
            SettingsViewModel)

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

    def open_file(self, path: str):
        """Centralized logic for opening a file."""
        try:
            with open(path, encoding="utf8") as f:
                content = f.read()
            editor_vm: CodeEditorViewModel = self.vm_store.get("DevTools")
            if editor_vm:
                editor_vm.open_script(path, content)
                AppLogger.get().info(f"📂 Opened in editor: {path}")
            else:
                AppLogger.get().warning("DevTools ViewModel not found.")
        except Exception as e:
            AppLogger.get().error(f"Failed to open {path}: {e}")

    def on_file_selected(self, path: str):
        """Callback for when a file is selected."""
        AppLogger.get().info(f"File selected: {path}")
        self.open_file(path)

    def handle_shortcuts(self):
        io = imgui.get_io()

        self.last_shortcut_frame = getattr(self, "last_shortcut_frame", -1)

        # Retrieve the active context
        active_context = self.application_data.app_settings.context_manager.get_active_context()

        # Check for shortcuts in the active context
        shortcuts = self.application_data.app_settings.shortcut_manager.get_shortcuts()
        for category, actions in shortcuts.items():
            for action, shortcut in actions.items():
                if shortcut == "Ctrl+O" and io.key_ctrl and imgui.is_key_pressed(imgui.Key.o, repeat=False):
                    current_frame = imgui.get_frame_count()
                    if current_frame != self.last_shortcut_frame:
                        self.last_shortcut_frame = current_frame
                        self.file_dialog.open()
                        AppLogger.get().info("Ctrl+O pressed – opening file dialog")
                        return


    def create_dockable_windows(self):
        AppLogger.get().debug(f"Creating dockable windows")
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
        AppLogger.get().debug(f"Creating runner params")
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
    ):
        AppLogger.get().debug(f"Registering Panel: {name} with {view_cls.__name__}")
        if name in self.panels:
            AppLogger.get().warning(f"Panel '{name}' already exists. Skipping registration.")
            return
        vm = viewmodel_cls(self)
        panel = view_cls(vm)
        self.vm_store[name] = vm
        self.panels[name] = panel

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