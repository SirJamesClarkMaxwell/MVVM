import os
from typing import Any, List

from imgui_bundle import hello_imgui, imgui

from core.file_dialog import FileDialogController
# import hello_imgui
from core.logger import AppLogger
from core.thread_pool import ThreadPool
from data import *
from models import *
from viewmodels import *
from viewmodels.shortcut_viewmodel import ShortcutViewModel
from views import *
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
        
        self.application_data.app_settings.shortcut_manager.bind_viewmodel_targets({
        "file_panel_viewmodel.open_file": self.file_dialog.open,
        "code_editor_viewmodel.save": self.vm_store["DevTools"].save_script,
        "app_viewmodel.close_active_window": self.close_active_window
    })
        
        runner_params = self.create_runner_params()
        runner_params.docking_params.dockable_windows = self.dockable_windows
        return runner_params

    def setup_panels(self):
        AppLogger.get().debug("Setting up panels")
        self.register_panel(
            name="Calculator",
            view_cls=CalculatorPanel,
            viewmodel_cls=CalculatorViewModel

        )
        self.register_panel(
            name="DevTools",
            view_cls=CodeEditorPanel,
            viewmodel_cls=CodeEditorViewModel
        )
        self.register_panel(
            name="Terminal",
            view_cls=TerminalPanel,
            viewmodel_cls=TerminalViewModel
        )
        self.register_panel(
            name="Settings",
            view_cls=SettingsPanel,
            viewmodel_cls=SettingsViewModel,
            view_args=[ShortcutViewModel()])

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
        keys = []
        for key in range(513,666):
            modifiers = []
            if io.key_ctrl:
                modifiers.append("Ctrl")
            if io.key_shift:
                modifiers.append("Shift")
            if io.key_alt:
                modifiers.append("Alt")
            if io.key_super:
                modifiers.append("Super")
            key_name = imgui.get_key_name(imgui.Key(key))
            if not key_name:
                continue
            full_key = "+".join(modifiers + [key_name])
            keys.append(full_key)

        if keys:
            self.vm_store["Settings"].handle_key_event(keys)

    def create_dockable_windows(self):
        AppLogger.get().debug("Creating dockable windows")
        for label in self.panels.keys():
            self.add_dockable_window_for_panel(label)

        log_window = hello_imgui.DockableWindow()
        log_window.label = "Logs"
        log_window.dock_space_name = "MainDockSpace"
        log_window.gui_function = hello_imgui.log_gui
        self.dockable_windows.append(log_window)

        self.file_dialog = FileDialogController()
        self.file_dialog.result_callback = lambda path: self.on_file_selected(
            path)

    def add_dockable_window_for_panel(self, label):
        window = hello_imgui.DockableWindow()
        window.label = label
        window.dock_space_name = "MainDockSpace"
        window.gui_function = lambda label=label: self.render_panel(label)
        self.dockable_windows.append(window)

    def create_runner_params(self):
        AppLogger.get().debug("Creating runner params")
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
        view_args: List[Any] | None = None,
        viewmodel_args: List[Any] | None = None,
        view_kwargs: dict[str, Any] | None = None,
        viewmodel_kwargs: dict[str, Any] | None = None,
    ):
        AppLogger.get().debug(
            f"Registering Panel: {name} with {view_cls.__name__}")
        if name in self.panels:
            AppLogger.get().warning(
                f"Panel '{name}' already exists. Skipping registration.")
            return
        vm = viewmodel_cls(self, 
                           *(viewmodel_args if viewmodel_args is not None else []),
                           **(viewmodel_kwargs if viewmodel_kwargs is not None else {}))
        panel = view_cls(vm, 
                        *(view_args if view_args is not None else []), 
                        **(view_kwargs if view_kwargs is not None else {}))
        self.vm_store[name] = vm
        self.panels[name] = panel

    def initialize_app_state(self):
        AppLogger.get().info("Initializing App state")
        self._shortcuts_initialization()
        self._scripting_initialization()

    def _scripting_initialization(self)->None:
        AppLogger.get().info("Initializing Scripting")
        try:
            editor_vm = self.vm_store["DevTools"]
            if not editor_vm:
                AppLogger.get().error(f"There are not DevTools panel")
                return None
            path = os.path.join(
                    os.path.abspath(os.path.curdir), "Scripts", "live_plot.py"
                )
            if  not os.path.exists(path):
                AppLogger.get().error(f"{path} don't exist")
            content = ""
            with open(path, "r") as f:
                content = f.read()
            editor_vm.open_script(path, content)
            AppLogger.get().info(f"📂 Loaded script: {path}")
        except Exception as e:
            AppLogger.get().error(f"❌ Failed to auto-load live_plot.py: {e}")
    def _shortcuts_initialization(self)->None:
        AppLogger.get().info("Initializing Shortcut")
        settings_viewmodel = self.vm_store["Settings"]
        if not settings_viewmodel:
            AppLogger.get().warning("There are no Settings ViewModel")
            return None
        cwd = os.path.abspath(os.curdir)
        filepath = os.path.join(cwd,"config/shortcuts.json")

        settings_viewmodel.load_from_file(filepath)
        
        
    def close_active_window(self):
        # TODO: implement close_active_window to remove focused panel from view
        AppLogger.get().info("Requested to close active window (stub)")
