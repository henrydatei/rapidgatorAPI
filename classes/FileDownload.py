import dataclasses

@dataclasses.dataclass
class FileDownload:
    download_url: str
    delay: int