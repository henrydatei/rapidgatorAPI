import dataclasses

from typing import Optional

@dataclasses.dataclass
class File:
    name: str
    size: int
    hash: Optional[str] = None
    nb_downloads: Optional[int] = None
    file_id: Optional[str] = None
    mode: Optional[int] = None
    mode_label: Optional[str] = None
    folder_id: Optional[str] = None
    url: Optional[str] = None
    created: Optional[int] = None