import dataclasses

from typing import Optional

@dataclasses.dataclass
class CheckLinkResult:
    url: str
    filename: str
    status: str
    size: Optional[int] = None