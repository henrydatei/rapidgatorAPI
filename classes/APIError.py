import dataclasses
from typing import Optional

@dataclasses.dataclass
class APIError():
    status: int
    response: Optional[dict] = None
    details: Optional[str] = None
    
    def __post_init__(self):
        print(self.details)