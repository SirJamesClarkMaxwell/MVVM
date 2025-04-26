class SettingsViewModel:
    def __init__(self,app,*args,**kwargs) -> None:
        self.app = app
        self.app_settings = app.application_data.app_settings
        for key, value in kwargs.items():
            setattr(self, key, value)