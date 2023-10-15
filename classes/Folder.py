import dataclasses
from typing import Optional, List

from classes.File import File

@dataclasses.dataclass
class Folder:
    folder_id: str
    mode: int
    mode_label: str
    parent_folder_id: str
    name: str
    url: str
    nb_folders: int
    nb_files: int
    created: int
    size_files: int
    folders: Optional[List["Folder"]] = None
    files: Optional[List["File"]] = None