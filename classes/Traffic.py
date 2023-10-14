import dataclasses
from typing import Optional

@dataclasses.dataclass
class Traffic:
    total: Optional[str] = None
    left: Optional[int] = None