import dataclasses
from typing import Optional

@dataclasses.dataclass
class Upload:
    max_file_size: int
    nb_pipes: int