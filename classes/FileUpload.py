import dataclasses
from typing import Optional

from classes.File import File

@dataclasses.dataclass
class FileUpload:
    upload_id: str
    state: int
    state_label: str
    file: Optional[File] = None
    url: Optional[str] = None