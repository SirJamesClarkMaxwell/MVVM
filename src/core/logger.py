import logging
from imgui_bundle import hello_imgui


class AppLogger:
    _instance = None

    def __init__(self):
        # Setup standard python logger once
        self._python_logger = logging.getLogger("AppLogger")
        if not self._python_logger.hasHandlers():
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "[%(levelname)s] %(filename)s:%(lineno)d in %(funcName)s() - %(message)s"
            )

            handler.setFormatter(formatter)
            self._python_logger.addHandler(handler)
            self._python_logger.setLevel(logging.DEBUG)

        self.log("AppLogger initialized", level="info")

    @classmethod
    def get(cls):
        if not cls._instance:
            cls._instance = AppLogger()
        return cls._instance

    def log(self, msg: str, level: str = "info"):
        # Log to Hello ImGui
        level_map = {
            "info": hello_imgui.LogLevel.info,
            "debug": hello_imgui.LogLevel.debug,
            "warning": hello_imgui.LogLevel.warning,
            "error": hello_imgui.LogLevel.error,
        }
        hello_imgui.log(level_map.get(level.lower(), hello_imgui.LogLevel.info), msg)

        # Also log to standard Python logging
        log_func = getattr(self._python_logger, level.lower(), self._python_logger.info)
        log_func(msg,stacklevel=3)

    def info(self, msg: str):
        self.log(msg, "info")

    def debug(self, msg: str):
        self.log(msg, "debug")

    def warning(self, msg: str):
        self.log(msg, "warning")

    def error(self, msg: str):
        self.log(msg, "error")
