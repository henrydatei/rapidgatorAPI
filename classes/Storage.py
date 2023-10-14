import dataclasses
from typing import Optional

@dataclasses.dataclass
class Storage:
    total: Optional[str] = None
    left: Optional[int] = None