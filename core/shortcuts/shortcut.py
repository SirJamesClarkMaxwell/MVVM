from dataclasses import dataclass
from typing import List

@dataclass
class Shortcut:
    id: str
    keys: List[str]
    category: str
    context: List[str]
    description: str
    target: str
