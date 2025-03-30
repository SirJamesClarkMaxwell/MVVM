from abc import ABC, abstractmethod
import attr
from viewmodels import ViewModel


@attr.s
class Panel(ABC):
    view_model = attr.ib(type=ViewModel)

    @abstractmethod
    def render(self):
        pass
