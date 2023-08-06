from lementpro.builders import Build
from lementpro.data.user import User
from lementpro.sender import Sender


class ObjectTypes:
    """Service for working with ObjectTypes in UserGate Public API"""  
    def object_template(self, by_user: User, objectTypeId: int=None, RelatedObjectId: int=None, RelatedObjectAttributeKnownId: str=None):
        """Get objectType object template
        :return: ObjectType attributes paging info
        """
        request_data = Build(url="/api/object_types/{objectTypeId}/object_template").get(objectTypeId=objectTypeId,RelatedObjectId=RelatedObjectId,RelatedObjectAttributeKnownId=RelatedObjectAttributeKnownId,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def tree(self, by_user: User, objectTypeId: int=None):
        """Get object type tree.
        :return: Object type info
        """
        request_data = Build(url="/api/object_types/{objectTypeId}/tree").get(objectTypeId=objectTypeId,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def objects(self, by_user: User, objectTypeId: int=None, By: int=None, Page: int=None, Order: str=None, OrderBy: str=None, IsAnySubTypeAvailable: bool=None, SearchPhrase: str=None, IsArchived: bool=None, ObjectIds: list=None):
        """Get objectType objects.
        :return: ObjectType objects paging info
        """
        request_data = Build(url="/api/object_types/{objectTypeId}/objects").get(objectTypeId=objectTypeId,By=By,Page=Page,Order=Order,OrderBy=OrderBy,IsAnySubTypeAvailable=IsAnySubTypeAvailable,SearchPhrase=SearchPhrase,IsArchived=IsArchived,ObjectIds=ObjectIds,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def ui_settings(self, by_user: User, objectTypeId: int=None):
        """Get objectType ui settings.
        :return: ObjectType attributes paging info
        """
        request_data = Build(url="/api/object_types/{objectTypeId}/ui_settings").get(objectTypeId=objectTypeId,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def menu(self, by_user: User):
        """Get object_types menu
        :return: Menu list
        """
        request_data = Build(url="/api/object_types/menu").get()
        return Sender().send_request(request_data, by_user=by_user)
        