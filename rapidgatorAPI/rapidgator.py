import dataclasses
import requests
from dacite import from_dict
from typing import List, Optional

from classes.APIError import APIError
from classes.User import User

@dataclasses.dataclass
class RapidgatorAPI():
    username: str
    password: str
    two_factor_code: Optional[str] = None
    
    def __post_init__(self) -> Optional[APIError]:
        params = {
            "login": self.username,
            "password": self.password,
        }
        if self.two_factor_code:
            params["code"] = self.two_factor_code
        r = requests.post("https://rapidgator.net/api/v2/user/login", data=params)
        if r.json()["status"] != 200:
            return from_dict(APIError, r.json())
        else:
            self.token = r.json()["response"]["token"]
            
    def info(self) -> User:
        params = {
            "token": self.token
        }
        r = requests.get("https://rapidgator.net/api/v2/user/info", params=params)
        if r.json()["status"] != 200:
            raise from_dict(APIError, r.json())
        else:
            return from_dict(User, r.json()["response"]["user"])