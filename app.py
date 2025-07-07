from inspect import Traceback
import os, sys
from typing import Any, List, Self, Type
from webbrowser import get
import json
from imgui_bundle import ImVec4, hello_imgui, imgui

from core import *
from data import *
from models import *
from presenters import *
from views import *


class App:
    _instance = None

    def __init__(self,*args):
        App._instance = self
        self.panels: dict[str, Panel] = {}
        self.dockable_windows: List[hello_imgui.DockableWindow] = []
        self.vm_store: dict[str:Any] = {}  # optional: {"calculator": vm, ...}
        self.thread_pool = ThreadPool()
        self.application_data = ApplicationData()
        self.file_dialog = FileDialogController(self)
        self.__project_path = os.path.abspath(os.curdir)
        self._running = True
        self.__handle_main_arguments(*args)
        self._runner_params = self.initialize()
        hello_imgui.manual_render.setup_from_runner_params(self._runner_params)

    def initialize(self,*args,**kwargs):
        AppLogger.get().info("Initializing App")
        self.setup_panels()
        self.__initialize_app_state(*args,**kwargs)

        return self.__create_runner_params()

    def run(self) -> None:
        while self._running:
            self.__handle_shortcuts()
            # NOTE: here is running self._render function. Handled by hello_imgui
            hello_imgui.manual_render.render()

            completed_tasks = self.thread_pool.get_completed()
            for task in completed_tasks:
                result = task.result()
                if result is not None:
                    AppLogger.get().info(f"Finished task {task.label}")
            if self._running:
                self._running = not hello_imgui.get_runner_params().app_shall_exit

    def shutdown(self):
        self.save_state()
        hello_imgui.manual_render.tear_down()

    def setup_panels(self):
        AppLogger.get().debug("Setting up panels")
        self.__register_panel(
            name="Calculator",
            view_cls=CalculatorPanel,
            presenter_cls=CalculatorPresenter,
            data_cls=CalculatorData,
        )

        self.__register_panel(
            name="DevTools",
            view_cls=CodeEditorPanel,
            presenter_cls=CodeEditorPresenter,
            data_cls=CodeEditorData,
        )

        shortcutPresenter = ShortcutPresenter(data=None, app=self)
        self.__register_panel(
            name="Settings",
            view_cls=SettingsPanel,
            presenter_cls=SettingsPresenter,
            data_cls=AppSettings,
            presenter_kwargs={"shortcut_presenter": shortcutPresenter},
            view_kwargs={
                "shortcut_presenter": shortcutPresenter
            },  
        )

        self.__create_dockable_windows()

    def __initialize_app_state(self):
        AppLogger.get().info("Initializing App state")
        self.__load_project()
        self._shortcuts_initialization()
        self._scripting_initialization()

    def __handle_main_arguments(self,*args):
        if not args:
            return ""
        if args:
            it = iter(args)
            for key in it:
                value = next(it, None)
                setattr(self, key.lstrip("-"), value)

    def __create_runner_params(self):
        AppLogger.get().debug("Creating runner params")
        params = hello_imgui.RunnerParams()
        params.app_window_params.window_title = "MVVM Paradise"
        # params.app_window_params.borderless = True
        params.app_window_params.borderless_highlight_color = ImVec4(0, 0, 0.11, 1)
        params.app_window_params.restore_previous_geometry = True
        params.app_window_params.window_geometry.full_screen_mode = (
            hello_imgui.FullScreenMode.full_monitor_work_area
        )

        # params.imgui_window_params.show_menu_bar = True
        params.imgui_window_params.show_menu_bar = True
        params.imgui_window_params.show_menu_app = False
        params.imgui_window_params.show_menu_view = True
        params.imgui_window_params.show_menu_app_quit = False

        params.callbacks.show_menus = self.__show_menus

        params.imgui_window_params.enable_viewports = True
        params.docking_params.dockable_windows = self.dockable_windows
        params.imgui_window_params.default_imgui_window_type = (
            hello_imgui.DefaultImGuiWindowType.provide_full_screen_dock_space
            | hello_imgui.DefaultImGuiWindowType.provide_full_screen_window
        )
        if os.path.exists(self.project_path + "\\MVVM_Paradise.ini"):
            AppLogger.get().debug(
                f"Settings UI from {self.__project_path}\\MVVM_Paradise.ini file"
            )
            params.ini_filename = self.__project_path + "MVVM_Paradise.ini"
        else:
            AppLogger.get().debug(
                f"No UI file detected in path  {self.__project_path}/MVVM_Paradise.ini"
            )

        return params

    def __show_menus(self):
        if imgui.begin_menu("Application"):
            _,quit_clicked = imgui.menu_item("Quit","ctrl+shift+w",False)
            if quit_clicked:
                AppLogger.get().info("App is closing")
                hello_imgui.get_runner_params().app_shall_exit = True
            imgui.end_menu()

    def __handle_shortcuts(self):
        io = imgui.get_io()
        keys = []
        self.last_shortcut_frame = getattr(self, "last_shortcut_frame", -1)
        for key in range(513, 666):
            if imgui.is_key_pressed(imgui.Key(key),repeat=False):
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
                if key_name:
                    full_key = "+".join(modifiers + [key_name])
                    keys.append(full_key)

        if keys and (self.last_shortcut_frame != imgui.get_frame_count()):
            self.last_shortcut_frame = imgui.get_frame_count()
            self.vm_store["Settings"].shortcut_presenter.handle_shortcut(keys)

    def __create_dockable_windows(self):
        AppLogger.get().debug("Creating dockable windows")
        for name, panel in self.panels.items():
            self.dockable_windows.append(panel.window)

        log_window = hello_imgui.DockableWindow()
        log_window.label = "Logs"
        log_window.dock_space_name = "MainDockSpace"
        log_window.gui_function = hello_imgui.log_gui
        self.dockable_windows.append(log_window)

    def __register_panel(
        self,
        name: str,
        view_cls,
        presenter_cls,
        data_cls=None,
        view_args: List[Any] | None = None,
        presenter_args: List[Any] | None = None,
        view_kwargs: dict[str, Any] | None = None,
        presenter_kwargs: dict[str, Any] | None = None,
    ):
        AppLogger.get().debug(f"Registering Panel: {name} with {view_cls.__name__}")
        if name in self.panels:
            AppLogger.get().warning(
                f"Panel '{name}' already exists. Skipping registration."
            )
            return
        if data_cls is not None:
            self.application_data[name] = data_cls()
        vm = presenter_cls(
            self.application_data[name],
            self,
            *(presenter_args if presenter_args is not None else []),
            **(presenter_kwargs if presenter_kwargs is not None else {}),
        )
        panel = view_cls(
            vm,
            *(view_args if view_args is not None else []),
            **(view_kwargs if view_kwargs is not None else {}),
        )
        self.vm_store[name] = vm
        self.panels[name] = panel

    def _scripting_initialization(self) -> None:
        AppLogger.get().info("Initializing Scripting")
        try:
            editor_vm = self.vm_store["DevTools"]
            if not editor_vm:
                AppLogger.get().error("There are not DevTools panel")
                return None
            path_lp = os.path.join(
                os.path.abspath(os.path.curdir), "src","Scripts", "live_plot.py"
            )
            path_test = os.path.join(
                os.path.abspath(os.path.curdir), "src","Scripts", "test_script.py")
            editor_vm.open_script(path_lp)
            editor_vm.open_script(path_test)
            AppLogger.get().info(f"📂 Loaded script: {path_lp} and {path_test}")
        except OSError as e:
            AppLogger.get().error(f"❌ Failed to auto-load live_plot.py: {e}")

    def _shortcuts_initialization(self) -> None:
        AppLogger.get().info("Initializing Shortcut")
        settings_presenter = self.vm_store.get("Settings")
        if not settings_presenter:
            AppLogger.get().warning("There is no Settings Presenter")
            return

        shortcut_presenter = getattr(settings_presenter, "shortcut_presenter", None)
        if not shortcut_presenter:
            AppLogger.get().warning(
                "Settings Presenter does not have a shortcut_presenter"
            )
            return

        cwd = os.path.abspath(os.curdir)
        filepath = os.path.join(cwd, ".\src\config\default_shortcuts.json")

        try:
            loaded_shortcuts = shortcut_presenter.load_from_file(filepath)
            bindings = create_global_shortcut_bindings(self)
            bindings += create_dev_tool_shortcut_binding(self)
            loaded_shortcuts.sort()
            bindings.sort()
            for shortcut,bind in zip(loaded_shortcuts,bindings):
                shortcut_presenter.bind_shortcut(shortcut, bind)
                shortcut_presenter.shortcut_registry.register(shortcut)
        except OSError as e:
            AppLogger.get().error(f"Failed to load shortcuts from {filepath}: {e}")

    def __load_project(self):
        project_path = getattr(self, "path", None)
        if not project_path:
            AppLogger.get().warning("No --path argument provided. Skipping project load.")
            return

        if not project_path.lower().endswith(".json"):
            AppLogger.get().error(f"Project file must be a .proj file: {project_path}")
            return

        if not os.path.isfile(project_path):
            AppLogger.get().error(f"Project file does not exist: {project_path}")
            return

        try:
            with open(project_path, "r", encoding="utf-8") as f:     
                project_data = json.load(f)
                self.__load_project_from_data(project_data)
            AppLogger.get().info(f"Loaded project from {project_path}")
        except Exception as e:
            AppLogger.get().error(f"Failed to load project file {project_path}: {e}")

    def __load_project_from_data(self,data:Any)->None:
        # TODO: Use project_data to initialize application state as needed
        pass
    def save_state(self) -> None:
        # TODO : implement save_state to save the current state of the application
        AppLogger.get().info("Saving application state (stub)")

    def __enter__(self) -> Self:
        AppLogger.get().info("Entering App context")
        return self

    def __exit__(self, 
                exc_type:Type[BaseException]|None,
                exc_val:Any|None,
                exc_tb:Traceback|None):
        AppLogger.get().info("Exiting App context")
        AppLogger.get().debug(str(exc_type))
        AppLogger.get().debug(str(exc_val))
        AppLogger.get().debug(str(exc_tb))
        self.shutdown()

    def set_context(self,context:str)->None:
        AppLogger.get().debug(f"New context {context}")
        self.vm_store["Settings"].shortcut_presenter.set_context(context)

    @property
    def context(self)->str:
        return self.vm_store["Settings"].shortcut_presenter.context

    @property
    def running(self)->bool:
        return self._running
    @running.setter
    def running(self,run:bool)->None:
        self._running = run

    @property
    def project_path(self) -> str:
        return self.__project_path
