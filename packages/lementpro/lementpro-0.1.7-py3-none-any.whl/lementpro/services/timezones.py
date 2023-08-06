from lementpro.builders import Build
from lementpro.data.user import User
from lementpro.sender import Sender


class TimeZones:
    """Service for working with TimeZones in UserGate Public API"""  
    def timezones(self, by_user: User, By: int=None, Page: int=None, Order: str=None, OrderBy: str=None, SearchString: str=None):
        """Get timezones by list
        :return: TimeZones paging model
        """
        request_data = Build(url="/api/timezones").get(By=By,Page=Page,Order=Order,OrderBy=OrderBy,SearchString=SearchString,)
        return Sender().send_request(request_data, by_user=by_user)
        