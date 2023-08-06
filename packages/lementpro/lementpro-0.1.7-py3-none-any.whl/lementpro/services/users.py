from lementpro.builders import Build
from lementpro.data.user import User
from lementpro.sender import Sender


class Users:
    """Service for working with Users in UserGate Public API"""  
    def users(self, by_user: User, DateCreatedFrom: str=None, DateCreatedTo: str=None, IsSystem: bool=None, Roles: list=None, IsDismissed: bool=None, IsDisabled: bool=None, By: int=None, Page: int=None, Order: str=None, OrderBy: str=None, SearchString: str=None, SearchStringExact: bool=None, DepartmentIds: list=None, RootDepartment: bool=None, UserIds: list=None, GroupId: int=None, GroupIntersect: bool=None, UserName: str=None, Emails: list=None, CanBeNotifiedInScopeOfVacation: bool=None, ReceiveNotificationByEmail: bool=None, ReceiveNotificationOnNewObject: bool=None, ReceiveNotificationOnChangedObject: bool=None, ReceiveNotificationOnlyOnChangeInFavoriteObjects: bool=None, ReceiveNotificationOnMentioned: bool=None):
        """Get users info by list
        :return: User paging extended info
        """
        request_data = Build(url="/api/users").get(DateCreatedFrom=DateCreatedFrom,DateCreatedTo=DateCreatedTo,IsSystem=IsSystem,Roles=Roles,IsDismissed=IsDismissed,IsDisabled=IsDisabled,By=By,Page=Page,Order=Order,OrderBy=OrderBy,SearchString=SearchString,SearchStringExact=SearchStringExact,DepartmentIds=DepartmentIds,RootDepartment=RootDepartment,UserIds=UserIds,GroupId=GroupId,GroupIntersect=GroupIntersect,UserName=UserName,Emails=Emails,CanBeNotifiedInScopeOfVacation=CanBeNotifiedInScopeOfVacation,ReceiveNotificationByEmail=ReceiveNotificationByEmail,ReceiveNotificationOnNewObject=ReceiveNotificationOnNewObject,ReceiveNotificationOnChangedObject=ReceiveNotificationOnChangedObject,ReceiveNotificationOnlyOnChangeInFavoriteObjects=ReceiveNotificationOnlyOnChangeInFavoriteObjects,ReceiveNotificationOnMentioned=ReceiveNotificationOnMentioned,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def post_mailbox(self, by_user: User, login: str=None, password: str=None, smtpHost: str=None, smtpPort: int=None, imapHost: str=None, imapPort: int=None, isDisabled: bool=None, signature: str=None):
        """Create new mailbox.
        :return: Created mailbox identifier
        """
        request_data = Build(url="/api/users/mailbox").post(login=login,password=password,smtpHost=smtpHost,smtpPort=smtpPort,imapHost=imapHost,imapPort=imapPort,isDisabled=isDisabled,signature=signature,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def patch_mailbox(self, by_user: User, login: str=None, password: str=None, smtpHost: str=None, smtpPort: int=None, imapHost: str=None, imapPort: int=None, isDisabled: bool=None, signature: str=None):
        """Partial update mailbox by id.
        :return: Empty
        """
        request_data = Build(url="/api/users/mailbox").patch(login=login,password=password,smtpHost=smtpHost,smtpPort=smtpPort,imapHost=imapHost,imapPort=imapPort,isDisabled=isDisabled,signature=signature,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def get_mailbox(self, by_user: User):
        """Get mailbox detailed info by id.
        :return: Mailbox info
        """
        request_data = Build(url="/api/users/mailbox").get()
        return Sender().send_request(request_data, by_user=by_user)
          
    def delete_mailbox(self, by_user: User):
        """Delete mailbox by id.
        :return: No content
        """
        request_data = Build(url="/api/users/mailbox").delete()
        return Sender().send_request(request_data, by_user=by_user)
          
    def put_notification_settings(self, by_user: User, receiveNotificationByEmail: bool=None, receiveNotificationOnNewObject: bool=None, receiveNotificationOnChangedObject: bool=None, receiveNotificationOnlyOnChangeInFavoriteObjects: bool=None, receiveNotificationOnMentioned: bool=None, receiveNotificationInVacation: bool=None):
        """Update notification setting.
        :return: Empty
        """
        request_data = Build(url="/api/users/notification_settings").put(receiveNotificationByEmail=receiveNotificationByEmail,receiveNotificationOnNewObject=receiveNotificationOnNewObject,receiveNotificationOnChangedObject=receiveNotificationOnChangedObject,receiveNotificationOnlyOnChangeInFavoriteObjects=receiveNotificationOnlyOnChangeInFavoriteObjects,receiveNotificationOnMentioned=receiveNotificationOnMentioned,receiveNotificationInVacation=receiveNotificationInVacation,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def get_notification_settings(self, by_user: User):
        """Get notification settings.
        :return: Mailbox info
        """
        request_data = Build(url="/api/users/notification_settings").get()
        return Sender().send_request(request_data, by_user=by_user)
          
    def get_assistants(self, by_user: User):
        """Get user assistants
        :return: Assistant paging extended info
        """
        request_data = Build(url="/api/users/assistants").get()
        return Sender().send_request(request_data, by_user=by_user)
          
    def post_assistants(self, by_user: User, assistantId: int=None):
        """Add user assistant
        :return: User assistant id
        """
        request_data = Build(url="/api/users/assistants").post(assistantId=assistantId,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def userAssistantId(self, by_user: User):
        """Delete user assistant by id.
        :return: Empty
        """
        request_data = Build(url="/api/users/assistants/{userAssistantId}").delete()
        return Sender().send_request(request_data, by_user=by_user)
        