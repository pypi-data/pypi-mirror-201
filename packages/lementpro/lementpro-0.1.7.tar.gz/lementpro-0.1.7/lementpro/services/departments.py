from lementpro.builders import Build
from lementpro.data.user import User
from lementpro.sender import Sender


class Departments:
    """Service for working with Departments in UserGate Public API"""  
    def departments(self, by_user: User, DateCreatedFrom: str=None, DateCreatedTo: str=None, By: int=None, Page: int=None, Order: str=None, OrderBy: str=None, IsSystem: bool=None, NameExact: bool=None, Name: str=None, ParentId: int=None, IsHidden: bool=None, DepartmentIds: list=None):
        """Get departments
        :return: Department paging info
        """
        request_data = Build(url="/api/departments").get(DateCreatedFrom=DateCreatedFrom,DateCreatedTo=DateCreatedTo,By=By,Page=Page,Order=Order,OrderBy=OrderBy,IsSystem=IsSystem,NameExact=NameExact,Name=Name,ParentId=ParentId,IsHidden=IsHidden,DepartmentIds=DepartmentIds,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def tree(self, by_user: User):
        """Get departments tree
        :return: Departments tree info
        """
        request_data = Build(url="/api/departments/tree").get()
        return Sender().send_request(request_data, by_user=by_user)
        