from lementpro.builders import Build
from lementpro.data.user import User
from lementpro.sender import Sender
from lementpro.data.emailaddressmodel import EmailAddressModel


class Comments:
    """Service for working with Comments in UserGate Public API"""  
    def get_comments(self, by_user: User, ObjectIds: list=None, FileIds: list=None, CommentIds: list=None, UserId: int=None, By: int=None, Page: int=None, Order: str=None, OrderBy: str=None, DateCreatedFrom: str=None, DateCreatedTo: str=None, IsSystem: bool=None, NotViewedByUserId: int=None, ExternalId: str=None, HasExternalEmail: bool=None):
        """Get comments
        :return: Comment paging info
        """
        request_data = Build(url="/api/comments").get(ObjectIds=ObjectIds,FileIds=FileIds,CommentIds=CommentIds,UserId=UserId,By=By,Page=Page,Order=Order,OrderBy=OrderBy,DateCreatedFrom=DateCreatedFrom,DateCreatedTo=DateCreatedTo,IsSystem=IsSystem,NotViewedByUserId=NotViewedByUserId,ExternalId=ExternalId,HasExternalEmail=HasExternalEmail,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def post_comments(self, by_user: User, objectId: int=None, objectName: str=None, message: str=None, parentId: int=None, emailAddress: EmailAddressModel=None, mentionedUserIds: list=None, fileIds: list=None):
        """Create new comment.
        :return: Created Comment identifier
        """
        request_data = Build(url="/api/comments").post(objectId=objectId,objectName=objectName,message=message,parentId=parentId,emailAddress=emailAddress,mentionedUserIds=mentionedUserIds,fileIds=fileIds,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def patch_commentId(self, by_user: User, message: str=None, emailAddress: EmailAddressModel=None, mentionedUserIds: list=None, fileIds: list=None):
        """Update comment by id.
        :return: No content
        """
        request_data = Build(url="/api/comments/{commentId}").patch(message=message,emailAddress=emailAddress,mentionedUserIds=mentionedUserIds,fileIds=fileIds,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def delete_commentId(self, by_user: User):
        """Delete Comment by id.
        :return: No content
        """
        request_data = Build(url="/api/comments/{commentId}").delete()
        return Sender().send_request(request_data, by_user=by_user)
          
    def mentions(self, by_user: User, By: int=None, Page: int=None, Order: str=None, OrderBy: str=None):
        """Get UserMentions
        :return: UserMention paging info
        """
        request_data = Build(url="/api/comments/mentions").get(By=By,Page=Page,Order=Order,OrderBy=OrderBy,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def remove(self, by_user: User, commentIds: list=None):
        """Delete UserMentions by comment identifiers
        :return: Empty
        """
        request_data = Build(url="/api/comments/mentions/remove").post(commentIds=commentIds,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def post_views(self, by_user: User, commentIds: list=None):
        """Create new UserView.
        :return: Created UserView identifier
        """
        request_data = Build(url="/api/comments/views").post(commentIds=commentIds,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def get_views(self, by_user: User, CommentId: int=None, By: int=None, Page: int=None, Order: str=None, OrderBy: str=None):
        """Get UserViews
        :return: UserView paging info
        """
        request_data = Build(url="/api/comments/views").get(CommentId=CommentId,By=By,Page=Page,Order=Order,OrderBy=OrderBy,)
        return Sender().send_request(request_data, by_user=by_user)
        