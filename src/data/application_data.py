from re import L
from typing import Any
from dataclasses import dataclass, field

from src.core.logger import AppLogger
from data.app_settings import AppSettings
from .code_editor_data import CodeEditorData
from .calculator_data import CalculatorData

@dataclass
class ApplicationData:
    panels_data:dict[str,Any] = field(default_factory=dict)
    open_file_dialog_requested: bool = False

    def __getitem__(self,name:str):
        if name not in self.panels_data.keys():
            AppLogger.get().error("You are trying to a not registered {name} data")
            raise ValueError("You are trying to a not registered {name} data")
        return self.panels_data[name]
    def __setitem__(self,name:str,item:Any)->None:
        if name not in self.panels_data.keys():
            self.panels_data[name] = item
        else:
            AppLogger.get().error("You are trying to a not registered {name} data")
