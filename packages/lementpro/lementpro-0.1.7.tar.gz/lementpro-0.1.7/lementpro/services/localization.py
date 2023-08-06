from lementpro.builders import Build
from lementpro.data.user import User
from lementpro.sender import Sender


class Localization:
    """Service for working with Localization in UserGate Public API"""  
    def etag(self, by_user: User):
        """Get localization resources last modified eTag
        :return: ETag info model
        """
        request_data = Build(url="/api/localization/cache/etag").get()
        return Sender().send_request(request_data, by_user=by_user)
          
    def export(self, by_user: User, Language: str=None, FileName: str=None, Tags: list=None):
        """Export localization dictionary of concrete language to json file
        :return: file, json
        """
        request_data = Build(url="/api/localization/export").get(Language=Language,FileName=FileName,Tags=Tags,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def locales(self, by_user: User):
        """Get locales by list
        :return: List of locales
        """
        request_data = Build(url="/api/localization/locales").get()
        return Sender().send_request(request_data, by_user=by_user)
        