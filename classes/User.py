import dataclasses

from classes.Traffic import Traffic
from classes.Storage import Storage
from classes.Upload import Upload
from classes.RemoteUpload import RemoteUpload

@dataclasses.dataclass
class User:
    email: str
    is_premium: bool
    state: int
    state_label: str
    traffic: Traffic
    storage: Storage
    upload: Upload
    remote_upload: RemoteUpload