from imgui_bundle import hello_imgui

class AppLogger:
    _instance = None

    def __init__(self):
        self.log("AppLogger initialized", level="info")

    @classmethod
    def get(cls):
        if not cls._instance:
            cls._instance = AppLogger()
        return cls._instance

    def log(self, msg: str, level: str = "info"):
        level_map = {
            "info": hello_imgui.LogLevel.info,
            "debug": hello_imgui.LogLevel.debug,
            "warning": hello_imgui.LogLevel.warning,
            "error": hello_imgui.LogLevel.error,
        }
        hello_imgui.log(level_map.get(level.lower(), hello_imgui.LogLevel.info), msg)

    def info(self, msg: str): self.log(msg, "info")
    def debug(self, msg: str): self.log(msg, "debug")
    def warning(self, msg: str): self.log(msg, "warning")
    def error(self, msg: str): self.log(msg, "error")
