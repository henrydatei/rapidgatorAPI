import dataclasses

@dataclasses.dataclass
class Pager:
    current: int
    total: int