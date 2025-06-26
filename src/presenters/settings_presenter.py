from src.data.app_settings import AppSettings
class SettingsPresenter:
    def __init__(self,app,data,*args,**kwargs) -> None:
        self.app = app
        self.data:AppSettings = data
        for key, value in kwargs.items():
            setattr(self, key, value)