from lementpro.builders import Build
from lementpro.data.user import User
from lementpro.sender import Sender


class Files:
    """Service for working with Files in UserGate Public API"""  
    def info(self, by_user: User, By: int=None, Page: int=None, Order: str=None, OrderBy: str=None, FileIds: list=None, FileGroupId: int=None, SearchString: str=None, SearchStringExact: bool=None):
        """Get files info by filter
        :return: File stream content
        """
        request_data = Build(url="/api/files/info").get(By=By,Page=Page,Order=Order,OrderBy=OrderBy,FileIds=FileIds,FileGroupId=FileGroupId,SearchString=SearchString,SearchStringExact=SearchStringExact,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def image(self, by_user: User, fileId: int=None, Width: int=None, Height: int=None):
        """Get resized image by file id
        :return: File stream content
        """
        request_data = Build(url="/api/files/{fileId}/image").get(fileId=fileId,Width=Width,Height=Height,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def get_fileId(self, by_user: User, fileId: int=None):
        """Get file by id.
        :return: File stream content
        """
        request_data = Build(url="/api/files/{fileId}").get(fileId=fileId,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def delete_fileId(self, by_user: User):
        """Delete file by id
        :return: Success
        """
        request_data = Build(url="/api/files/{fileId}").delete()
        return Sender().send_request(request_data, by_user=by_user)
          
    def temp(self, by_user: User):
        """Upload file as temp
        :return: File stream content
        """
        request_data = Build(url="/api/files/temp").post()
        return Sender().send_request(request_data, by_user=by_user)
          
    def files(self, by_user: User):
        """Upload file as permanent
        :return: File stream content
        """
        request_data = Build(url="/api/files").post()
        return Sender().send_request(request_data, by_user=by_user)
          
    def download_archive(self, by_user: User, ids: list=None):
        """Download archive from multiple files.
        :return: File stream content
        """
        request_data = Build(url="/api/files/download_archive").get(ids=ids,)
        return Sender().send_request(request_data, by_user=by_user)
        