from dataclasses import dataclass,field
from typing import List,Callable,Optional

@dataclass
class Shortcut:
    id: str
    keys: List[str]
    category: str
    context: List[str]
    description: str
    function: Optional[Callable] = field(default=None)
