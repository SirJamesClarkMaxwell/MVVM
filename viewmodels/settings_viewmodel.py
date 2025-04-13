
from data.app_settings import AppSettings

class SettingsViewModel:
    def __init__(self,app) -> None:
        self.app = app
        self.app_settings = AppSettings()
        pass