import dataclasses

from classes.File import File

@dataclasses.dataclass
class OneTimeLink:
    link_id: str
    file: File
    url: str
    state: str
    state_label: str
    callback_url: str
    notify: bool
    created: int
    downloaded: bool