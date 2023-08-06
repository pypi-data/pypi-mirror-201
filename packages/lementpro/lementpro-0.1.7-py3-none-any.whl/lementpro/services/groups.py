from lementpro.builders import Build
from lementpro.data.user import User
from lementpro.sender import Sender


class Groups:
    """Service for working with Groups in UserGate Public API"""  
    def groups(self, by_user: User, DateCreatedFrom: str=None, DateCreatedTo: str=None, By: int=None, Page: int=None, Order: str=None, OrderBy: str=None, IsSystem: bool=None, Name: str=None, NameExact: bool=None):
        """Get groups
        :return: Group paging info
        """
        request_data = Build(url="/api/groups").get(DateCreatedFrom=DateCreatedFrom,DateCreatedTo=DateCreatedTo,By=By,Page=Page,Order=Order,OrderBy=OrderBy,IsSystem=IsSystem,Name=Name,NameExact=NameExact,)
        return Sender().send_request(request_data, by_user=by_user)
        