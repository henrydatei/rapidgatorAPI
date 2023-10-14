import dataclasses
from typing import Optional

@dataclasses.dataclass
class RemoteUpload:
    max_nb_jobs: int
    refresh_time: int