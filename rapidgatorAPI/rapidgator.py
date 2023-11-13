import dataclasses
import requests
from dacite import from_dict
from typing import List, Optional, Tuple

from classes.APIError import APIError
from classes.User import User
from classes.Folder import Folder
from classes.Pager import Pager
from classes.File import File
from classes.FileUpload import FileUpload
from classes.FileDownload import FileDownload
from classes.OneTimeLink import OneTimeLink
from classes.CheckLinkResult import CheckLinkResult
from classes.RemoteUploadJob import RemoteUploadJob

@dataclasses.dataclass
class RapidgatorAPI():
    username: str
    password: str
    two_factor_code: Optional[str] = None
    
    def __post_init__(self) -> None:
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
        """Returns a list of the user's personal information.

        Raises:
            APIError: e.g. if user is not found

        Returns:
            User: The user's personal information
        """
        params = {
            "token": self.token
        }
        r = requests.get("https://rapidgator.net/api/v2/user/info", params=params)
        if r.json()["status"] != 200:
            raise from_dict(APIError, r.json())
        else:
            return from_dict(User, r.json()["response"]["user"])
        
    def folder_create(self, name: str, parent_folder_id: str = None) -> Folder:
        """Creates a folder.

        Args:
            name (str): The name of the folder to be created.
            parent_folder_id (str): The key that identifies the folder. If the parent_folder_id is not passed, will return the root folder details.

        Raises:
            APIError: e.g. if the parent folder is not found

        Returns:
            Folder: The created folder
        """
        params = {
            "token": self.token,
            "name": name
        }
        if parent_folder_id:
            params["folder_id"] = parent_folder_id
        r = requests.post("https://rapidgator.net/api/v2/folder/create", data=params)
        if r.json()["status"] != 200:
            raise from_dict(APIError, r.json())
        else:
            return from_dict(Folder, r.json()["response"]["folder"])
        
    def folder_info(self, folder_id: str = None) -> Folder:
        """Returns a folder's and list of sub folders details.

        Args:
            folder_id (str): The key that identifies the folder. If the folder_id is not passed, will return the root folder details.

        Raises:
            APIError: e.g. if the folder is not found

        Returns:
            Folder: The folder information
        """
        params = {
            "token": self.token
        }
        if folder_id:
            params["folder_id"] = folder_id
        r = requests.get("https://rapidgator.net/api/v2/folder/info", params=params)
        if r.json()["status"] != 200:
            raise from_dict(APIError, r.json())
        else:
            return from_dict(Folder, r.json()["response"]["folder"])
        
    def folder_content(self, folder_id: str = None, page: int = 1, per_page: int = 500, sort_column: str = "name", sort_direction: str = "ASC") -> Tuple[Folder, Pager]:
        """Returns a folder's, list of sub folders and list of files details.

        Args:
            folder_id (str): The key that identifies the folder. If the folder_id is not passed, will return the root folder details.
            page (int): Page number. Default is 1
            per_page (int): TNumber of files per page. Default is 500.
            sort_column (str): Sort column name. Possible values: 'name', 'created', 'size', 'nb_downloads'. Default is 'name'.
            sort_direction (str): Sort direction. Possible values: 'ASC', 'DESC'. Default is 'ASC'.

        Raises:
            APIError: e.g. if the folder is not found
            ValueError: e.g. if sort_column or sort_direction is invalid

        Returns:
            Folder: The folder information
        """
        params = {
            "token": self.token
        }
        if folder_id:
            params["folder_id"] = folder_id
        if page:
            params["page"] = page
        if per_page:
            params["per_page"] = per_page
        if sort_column:
            if sort_column not in ["name", "created", "size", "nb_downloads"]:
                raise ValueError("sort_column must be one of 'name', 'created', 'size', 'nb_downloads'")
            params["sort_column"] = sort_column
        if sort_direction:
            if sort_direction not in ["ASC", "DESC"]:
                raise ValueError("sort_direction must be one of 'ASC', 'DESC'")
            params["sort_direction"] = sort_direction
        r = requests.get("https://rapidgator.net/api/v2/folder/content", params=params)
        if r.json()["status"] != 200:
            raise from_dict(APIError, r.json())
        else:
            return Tuple(from_dict(Folder, r.json()["response"]["folder"]), from_dict(Pager, r.json()["response"]["pager"]))
        
    def folder_rename(self, folder_id: str, name: str) -> Folder:
        """Rename a folder.

        Args:
            folder_id (str): The key that identifies the folder to be renamed.
            name (str): The new name of the folder.

        Returns:
            Folder: The renamed folder
        """
        params = {
            "token": self.token,
            "folder_id": folder_id,
            "name": name
        }
        r = requests.post("https://rapidgator.net/api/v2/folder/rename", data=params)
        if r.json()["status"] != 200:
            raise from_dict(APIError, r.json())
        else:
            return from_dict(Folder, r.json()["response"]["folder"])
        
    def folder_copy(self, folder_id: str, folder_id_dest: str) -> dict:
        """Copy a folder to another folder (This operation also works with foreign folders).

        Args:
            folder_id (str): The key that identifies the folder to be copied.
            folder_id_dest (str): The key that identifies the destination folder.

        Returns:
            Folder: The copied folder
        """
        params = {
            "token": self.token,
            "folder_id": folder_id,
            "folder_id_dest": folder_id_dest
        }
        r = requests.post("https://rapidgator.net/api/v2/folder/copy", data=params)

        # Even if the folder is not found, the API returns a 200 status code. WTF?
        return r.json()["response"]
    
    def folder_move(self, folder_id: str, folder_id_dest: str) -> dict:
        """Move a folder to another folder (This operation also works with foreign folders).

        Args:
            folder_id (str): The key that identifies the folder to be moved.
            folder_id_dest (str): The key that identifies the destination folder.

        Returns:
            Folder: The moved folder
        """
        params = {
            "token": self.token,
            "folder_id": folder_id,
            "folder_id_dest": folder_id_dest
        }
        r = requests.post("https://rapidgator.net/api/v2/folder/move", data=params)

        # Even if the folder is not found, the API returns a 200 status code. WTF?
        return r.json()["response"]
    
    def folder_delete(self, folder_id: str) -> dict:
        """Delete a folder.

        Args:
            folder_id (str): The key that identifies the folder to be deleted.

        Returns:
            dict: The response
        """
        params = {
            "token": self.token,
            "folder_id": folder_id
        }
        r = requests.post("https://rapidgator.net/api/v2/folder/delete", data=params)

        # Even if the folder is not found, the API returns a 200 status code. WTF?
        return r.json()["response"]
    
    def folder_change_mode(self, folder_id: str, mode: int) -> Folder:
        """Change a folder mode.

        Args:
            folder_id (str): The key that identifies the folder to be changed.
            mode (int): The new mode of the folder. Possible values: 0 - Public, 1 - Premium only, 2 - Private, 3 - Hotlink.
            
        Raises:
            APIError: e.g. if the folder is not found
            ValueError: e.g. if mode is invalid

        Returns:
            Folder: The changed folder
        """
        if mode not in [0, 1, 2, 3]:
            raise ValueError("mode must be one of 0, 1, 2, 3")
        params = {
            "token": self.token,
            "folder_id": folder_id,
            "mode": mode
        }
        r = requests.post("https://rapidgator.net/api/v2/folder/change_mode", data=params)
        if r.json()["status"] != 200:
            raise from_dict(APIError, r.json())
        else:
            return from_dict(Folder, r.json()["response"]["folder"])
        
    def file_upload(self, name: str, hash: str, size: int, folder_id: int = None, multipart: bool = True) -> FileUpload:
        """Checks if instant upload is possible and return upload session object with file info or upload URL.
        
        Upload steps:
            1. Do file_upload API request. If upload state not equal 0 no need other steps.
            2. Upload file to upload url.
            3. Do file_upload_info API request.

        Args:
            name (str): The file name
            hash (str): MD5 hash of the file
            size (int): The file size
            folder_id (int): The key that identifies the folder. If the folder_id is not passed, will upload to the root folder.
            multipart (bool): This parameter indicates the type of upload. Default is true.

        Raises:
            APIError: e.g. you can't create more than 10 copies of the same file

        Returns:
            FileUpload: The uploaded file status
        """
        params = {
            "token": self.token,
            "name": name,
            "hash": hash,
            "size": size
        }
        if folder_id:
            params["folder_id"] = folder_id
        if multipart is not None:
            params["multipart"] = multipart
        r = requests.post("https://rapidgator.net/api/v2/file/upload", data=params)
        if r.json()["status"] != 200:
            raise from_dict(APIError, r.json())
        else:
            return from_dict(FileUpload, r.json()["response"]["upload"])
        
    def file_upload_info(self, upload_id: str) -> FileUpload:
        """Checks upload session state.

        Args:
            upload_id (str): The upload session id.

        Raises:
            APIError: e.g. if the upload id is not found

        Returns:
            FileUpload: The uploaded file status
        """
        params = {
            "token": self.token,
            "upload_id": upload_id
        }
        r = requests.get("https://rapidgator.net/api/v2/file/upload_info", params=params)
        if r.json()["status"] != 200:
            raise from_dict(APIError, r.json())
        else:
            return from_dict(FileUpload, r.json()["response"]["upload"])
        
    def file_download(self, file_id: str) -> FileDownload:
        """Download a file.

        Args:
            file_id (str): The key that identifies the file.

        Raises:
            APIError: e.g. if the file is not found

        Returns:
            FileDownload: The file download URL
        """
        params = {
            "token": self.token,
            "file_id": file_id
        }
        r = requests.get("https://rapidgator.net/api/v2/file/download", params=params)
        if r.json()["status"] != 200:
            raise from_dict(APIError, r.json())
        else:
            return from_dict(FileDownload, r.json()["response"]["file"])
        
    def file_info(self, file_id: str) -> File:
        """Returns a file's details.

        Args:
            file_id (str): The key that identifies the file.

        Raises:
            APIError: e.g. if the file is not found

        Returns:
            File: The file information
        """
        params = {
            "token": self.token,
            "file_id": file_id
        }
        r = requests.get("https://rapidgator.net/api/v2/file/info", params=params)
        if r.json()["status"] != 200:
            raise from_dict(APIError, r.json())
        else:
            return from_dict(File, r.json()["response"]["file"])
        
    def file_rename(self, file_id: str, name: str) -> File:
        """Rename a file.

        Args:
            file_id (str): The key that identifies the file to be renamed.
            name (str): The new name of the file.

        Returns:
            File: The renamed file
        """
        params = {
            "token": self.token,
            "file_id": file_id,
            "name": name
        }
        r = requests.post("https://rapidgator.net/api/v2/file/rename", data=params)
        if r.json()["status"] != 200:
            raise from_dict(APIError, r.json())
        else:
            return from_dict(File, r.json()["response"]["file"])
        
    def file_copy(self, file_id: str, folder_id_dest: str) -> dict:
        """Copy a file to another folder (This operation also works with foreign folders).

        Args:
            file_id (str): The key that identifies the file to be copied.
            folder_id_dest (str): The key that identifies the destination folder.
            
        Raises:
            APIError: e.g. if the destination folder is not found

        Returns:
            dict: The response
        """
        params = {
            "token": self.token,
            "file_id": file_id,
            "folder_id_dest": folder_id_dest
        }
        r = requests.post("https://rapidgator.net/api/v2/file/copy", data=params)

        if r.json()["status"] != 200:
            raise from_dict(APIError, r.json())
        else:
            return r.json()["response"]
        
    def file_xcopy(self, url: str, folder_id_dest: str) -> File:
        """Copy a file to another folder by download link.

        Args:
            url (str): The key that identifies the file to be copied.
            folder_id_dest (str): The key that identifies the destination folder.
            
        Raises:
            APIError: e.g. you can't create more than 10 copies of the same file

        Returns:
            File: The copied file
        """
        params = {
            "token": self.token,
            "url": url,
            "folder_id_dest": folder_id_dest
        }
        r = requests.post("https://rapidgator.net/api/v2/file/xcopy", data=params)

        if r.json()["status"] != 200:
            raise from_dict(APIError, r.json())
        else:
            return from_dict(File, r.json()["response"]["file"])
        
    def file_hashcopy(self, hash: str, folder_id_dest: str, name: str) -> File:
        """Copy a file to another folder by MD5 hash.

        Args:
            hash (str): The key that identifies the file to be copied.
            folder_id_dest (str): The key that identifies the destination folder.
            name (str): The new name of the file.
            
        Raises:
            APIError: e.g. if the file is not found

        Returns:
            File: The copied file
        """
        params = {
            "token": self.token,
            "hash": hash,
            "folder_id_dest": folder_id_dest
        }
        r = requests.post("https://rapidgator.net/api/v2/file/hashcopy", data=params)

        if r.json()["status"] != 200:
            raise from_dict(APIError, r.json())
        else:
            return from_dict(File, r.json()["response"]["file"])
        
    def file_move(self, file_id: str, folder_id_dest: str) -> dict:
        """Move a file to another folder (This operation also works with foreign folders).

        Args:
            file_id (str): The key that identifies the file to be moved.
            folder_id_dest (str): The key that identifies the destination folder.

        Returns:
            dict: The response
        """
        params = {
            "token": self.token,
            "file_id": file_id,
            "folder_id_dest": folder_id_dest
        }
        r = requests.post("https://rapidgator.net/api/v2/file/move", data=params)

        # Even if the file is not found, the API returns a 200 status code. WTF?
        return r.json()["response"]
    
    def file_delete(self, file_id: str) -> dict:
        """Delete a file.

        Args:
            file_id (str): The key that identifies the file to be deleted.

        Returns:
            dict: The response
        """
        params = {
            "token": self.token,
            "file_id": file_id
        }
        r = requests.post("https://rapidgator.net/api/v2/file/delete", data=params)

        # Even if the file is not found, the API returns a 200 status code. WTF?
        return r.json()["response"]
    
    def file_change_mode(self, file_id: str, mode: int) -> File:
        """Change a file mode.

        Args:
            file_id (str): The key that identifies the file to be changed.
            mode (int): The new mode of the file. Possible values: 0 - Public, 1 - Premium only, 2 - Private, 3 - Hotlink.
            
        Raises:
            APIError: e.g. if the file is not found
            ValueError: e.g. if mode is invalid

        Returns:
            File: The changed file
        """
        if mode not in [0, 1, 2, 3]:
            raise ValueError("mode must be one of 0, 1, 2, 3")
        params = {
            "token": self.token,
            "file_id": file_id,
            "mode": mode
        }
        r = requests.post("https://rapidgator.net/api/v2/file/change_mode", data=params)
        if r.json()["status"] != 200:
            raise from_dict(APIError, r.json())
        else:
            return from_dict(File, r.json()["response"]["file"])
        
    def file_check_link(self, url: str) -> List[CheckLinkResult]:
        """Check a file download link.

        Args:
            url (str): The file download link.
            
        Raises:
            APIError: e.g. to many links

        Returns:
            List[CheckLinkResult]: The check link result
        """
        params = {
            "token": self.token,
            "url": url
        }
        r = requests.get("https://rapidgator.net/api/v2/file/check_link", params=params)

        if r.json()["status"] != 200:
            raise from_dict(APIError, r.json())
        else:
            return [from_dict(CheckLinkResult, response) for response in r.json()["response"]]
        
    def file_onetimelink_create(self, file_id: str, callback_url: str = None, notify: bool = None) -> OneTimeLink:
        """Create a one time download link.

        Args:
            file_id (str): The key that identifies the file.
            callback_url (str): Callback URL. A callback URL will be invoked when file will be downloaded.
            notify (bool): Send notification letter when file will be downloaded
            
        Raises:
            APIError: e.g. if the file is not found

        Returns:
            OneTimeLink: The one time download link
        """
        params = {
            "token": self.token,
            "file_id": file_id
        }
        if callback_url:
            params["url"] = callback_url
        if notify is not None:
            params["notify"] = notify
        r = requests.post("https://rapidgator.net/api/v2/file/onetimelink_create", data=params)

        if r.json()["status"] != 200:
            raise from_dict(APIError, r.json())
        else:
            return from_dict(OneTimeLink, r.json()["response"]["link"])
        
    def file_onetimelink_info(self, link_id: str = None) -> List[OneTimeLink]:
        """Returns a one time download link details.

        Args:
            link_id (str): The key that identifies the one-time link. You can also specify multiple link keys separated by comma. If the link_id is not passed, will return all one-time link details.

        Raises:
            APIError: e.g. if the link is not found

        Returns:
            List[OneTimeLink]: The one time download link details
        """
        params = {
            "token": self.token,
            "link_id": link_id
        }
        r = requests.get("https://rapidgator.net/api/v2/file/onetimelink_info", params=params)

        if r.json()["status"] != 200:
            raise from_dict(APIError, r.json())
        else:
            return [from_dict(OneTimeLink, link) for link in r.json()["response"]["links"]]
        
    def trashcan_content(self, page: int = 1, per_page: int = 500, sort_column: str = "name", sort_direction: str = "ASC") -> Tuple[List[File], Pager]:
        """Returns a list of files in the trashcan.

        Args:
            page (int): Page number. Default is 1
            per_page (int): TNumber of files per page. Default is 500.
            sort_column (str): Sort column name. Possible values: 'name', 'created', 'size', 'delete_time'. Default is 'name'
            sort_direction (str): Sort direction. Possible values: 'ASC', 'DESC'. Default is 'ASC'.

        Raises:
            ValueError: e.g. if sort_column or sort_direction is invalid

        Returns:
            Tuple[List[File], Pager]: The list of files in the trashcan and the pager
        """
        params = {
            "token": self.token
        }
        if page:
            params["page"] = page
        if per_page:
            params["per_page"] = per_page
        if sort_column:
            if sort_column not in ["name", "created", "size", "delete_time"]:
                raise ValueError("sort_column must be one of 'name', 'created', 'size', 'delete_time'")
            params["sort_column"] = sort_column
        if sort_direction:
            if sort_direction not in ["ASC", "DESC"]:
                raise ValueError("sort_direction must be one of 'ASC', 'DESC'")
            params["sort_direction"] = sort_direction
        r = requests.get("https://rapidgator.net/api/v2/trashcan/content", params=params)
        if r.json()["status"] != 200:
            raise from_dict(APIError, r.json())
        else:
            return Tuple([from_dict(File, file) for file in r.json()["response"]["files"]], from_dict(Pager, r.json()["response"]["pager"]))
        
    def trashcan_restore(self, file_id: str = None) -> dict:
        """Restore a file from the trashcan to root folder.

        Args:
            file_id (str): The key that identifies the file. If not specified will be restored all files.

        Returns:
            dict: The response
        """
        params = {
            "token": self.token,
        }
        if file_id:
            params["file_id"] = file_id
        r = requests.post("https://rapidgator.net/api/v2/trashcan/restore", data=params)

        # Even if the file is not found, the API returns a 200 status code. WTF?
        return r.json()["response"]
    
    def trashcan_empty(self, file_id: str = None) -> dict:
        """Empty the trashcan.
        
        Args:
            file_id (str): The key that identifies the file. If not specified will be deleted all files.

        Returns:
            dict: The response
        """
        params = {
            "token": self.token,
        }
        if file_id:
            params["file_id"] = file_id
        r = requests.post("https://rapidgator.net/api/v2/trashcan/empty", data=params)

        # Even if the file is not found, the API returns a 200 status code. WTF?
        return r.json()["response"]
    
    def remote_upload_create(self, url: str) -> List[RemoteUploadJob]:
        """Create a remote upload job.

        Args:
            url (str): The URL of the file to be uploaded.
            
        Raises:
            APIError: e.g. Exceeded the storage quota

        Returns:
            List[RemoteUploadJob]: The remote upload job
        """
        params = {
            "token": self.token,
            "url": url
        }
        r = requests.post("https://rapidgator.net/api/v2/remote/create", data=params)

        if r.json()["status"] != 200:
            raise from_dict(APIError, r.json())
        else:
            return [from_dict(RemoteUploadJob, job) for job in r.json()["response"]["jobs"]]
        
    def remote_upload_info(self, job_id: int = None) -> List[RemoteUploadJob]:
        """Returns a remote upload job details.

        Args:
            job_id (int): The key that identifies the remote upload job. If the job_id is not passed, will return all remote upload job details.

        Returns:
            List[RemoteUploadJob]: The remote upload job details
        """
        params = {
            "token": self.token,
        }
        if job_id:
            params["job_id"] = job_id
        r = requests.get("https://rapidgator.net/api/v2/remote/info", params=params)

        return [from_dict(RemoteUploadJob, job) for job in r.json()["response"]["jobs"]]
    
    def remote_job_delete(self, job_id: int) -> dict:
        """Delete a remote upload job.

        Args:
            job_id (int): The key that identifies the remote upload job.

        Returns:
            dict: The response
        """
        params = {
            "token": self.token,
            "job_id": job_id
        }
        r = requests.post("https://rapidgator.net/api/v2/remote/delete", data=params)

        # Even if the job is not found, the API returns a 200 status code. WTF?
        return r.json()["response"]