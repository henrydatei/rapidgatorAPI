import dataclasses
from typing import Optional

from classes.File import File

@dataclasses.dataclass
class RemoteUploadJob:
    job_id: int
    type: int
    type_label: str
    folder_id: str
    url: str
    name: str
    size: int
    state: int
    state_label: str
    file: File
    dl_size: int
    speed: int
    created: int
    uploaded: Optional[int] = None
    error: Optional[str] = None