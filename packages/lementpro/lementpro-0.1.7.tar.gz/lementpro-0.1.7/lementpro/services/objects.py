from lementpro.builders import Build
from lementpro.data.user import User
from lementpro.sender import Sender
from lementpro.data.usergateobjectaddmodel import UserGateObjectAddModel


class Objects:
    """Service for working with Objects in UserGate Public API"""  
    def get_objectId(self, by_user: User, objectId: int=None):
        """Get object info by object identifier
        :return: Object user info
        """
        request_data = Build(url="/api/objects/{objectId}").get(objectId=objectId,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def patch_objectId(self, by_user: User, correctParentDates: bool=None, objectAttributes: list=None):
        """Partial update object by object identifier
        :return: No content
        """
        request_data = Build(url="/api/objects/{objectId}").patch(correctParentDates=correctParentDates,objectAttributes=objectAttributes,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def related_objects(self, by_user: User, objectId: int=None, By: int=None, Page: int=None, Order: str=None, OrderBy: str=None, AttributeKnownId: str=None):
        """
        :return: Success
        """
        request_data = Build(url="/api/objects/{objectId}/related_objects").get(objectId=objectId,By=By,Page=Page,Order=Order,OrderBy=OrderBy,AttributeKnownId=AttributeKnownId,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def steps(self, by_user: User, objectId: int=None):
        """Get all objects info of all steps by object id
        :return: List of all objects info inside all steps, incl. steps itself
        """
        request_data = Build(url="/api/objects/{objectId}/steps").get(objectId=objectId,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def objects(self, by_user: User, name: str=None, objectTypeId: int=None, correctParentDates: bool=None, bimElementIds: list=None, objectAttributes: list=None):
        """Create new object
        :return: Archive action info
        """
        request_data = Build(url="/api/objects").post(name=name,objectTypeId=objectTypeId,correctParentDates=correctParentDates,bimElementIds=bimElementIds,objectAttributes=objectAttributes,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def actionId(self, by_user: User, dateEnd: str=None, userIds: list=None, comment: str=None, relatedObjectIds: list=None, relationAttributeKnownId: str=None, newObject: UserGateObjectAddModel=None):
        """Execute object action.
        :return: Archive action info
        """
        request_data = Build(url="/api/objects/{objectId}/{actionId}").post(dateEnd=dateEnd,userIds=userIds,comment=comment,relatedObjectIds=relatedObjectIds,relationAttributeKnownId=relationAttributeKnownId,newObject=newObject,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def favorite(self, by_user: User, objectIds: list=None, isFavorite: bool=None):
        """Toggle favorite objects
        :return: No content
        """
        request_data = Build(url="/api/objects/favorite").post(objectIds=objectIds,isFavorite=isFavorite,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def read(self, by_user: User, objectIds: list=None):
        """Mark read pack of objects
        :return: No content
        """
        request_data = Build(url="/api/objects/read").post(objectIds=objectIds,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def unread(self, by_user: User, objectIds: list=None):
        """Mark unread pack of objects
        :return: No content
        """
        request_data = Build(url="/api/objects/unread").post(objectIds=objectIds,)
        return Sender().send_request(request_data, by_user=by_user)
        