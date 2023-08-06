from lementpro.builders import Build
from lementpro.data.user import User
from lementpro.sender import Sender


class Search:
    """Service for working with Search in UserGate Public API"""  
    def extended(self, by_user: User, By: int=None, Page: int=None, Order: str=None, OrderBy: str=None, ObjectTypeId: int=None, IsAnySubTypeAvailable: bool=None, SearchPhrase: str=None, IsArchived: bool=None):
        """Extended search.
        :return: Object type paging info
        """
        request_data = Build(url="/api/search/extended").get(By=By,Page=Page,Order=Order,OrderBy=OrderBy,ObjectTypeId=ObjectTypeId,IsAnySubTypeAvailable=IsAnySubTypeAvailable,SearchPhrase=SearchPhrase,IsArchived=IsArchived,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def quick(self, by_user: User, Phrase: str=None, By: int=None):
        """Quick search (by fixed objectTypes and limited results).
        :return: Object type paging info
        """
        request_data = Build(url="/api/search/quick").get(Phrase=Phrase,By=By,)
        return Sender().send_request(request_data, by_user=by_user)
        