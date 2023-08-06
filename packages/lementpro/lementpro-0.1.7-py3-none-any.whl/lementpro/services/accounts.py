from lementpro.builders import Build
from lementpro.data.user import User
from lementpro.sender import Sender
from lementpro.data.usermodelextension import UserModelExtension
from lementpro.data.usermodelnotification import UserModelNotification


class Accounts:
    """Service for working with Accounts in UserGate Public API"""

    def login(self, by_user: User, login: str = None, password: str = None):
        """Sign in by login
        :return: Access token model
        """
        request_data = Build(
            url="/api/accounts/login").post(login=login, password=password,)
        return Sender().send_request(request_data, by_user=by_user)

    def refresh_token(self, by_user: User, refreshToken: str = None):
        """Refresh token
        :return: Access token model
        """
        request_data = Build(
            url="/api/accounts/refresh_token").post(refreshToken=refreshToken,)
        return Sender().send_request(request_data, by_user=by_user)

    def logout(self, by_user: User):
        """Sign out
        :return: No Content
        """
        request_data = Build(url="/api/accounts/logout").post()
        return Sender().send_request(request_data, by_user=by_user)

    def restore_password(self, by_user: User, login: str = None, companyId: int = None):
        """Restore password
        :return: No Content
        """
        request_data = Build(
            url="/api/accounts/restore_password").post(login=login, companyId=companyId,)
        return Sender().send_request(request_data, by_user=by_user)

    def get_me(self, by_user: User):
        """Get me
        :return: Created BlockWork identifier
        """
        request_data = Build(url="/api/accounts/me").get()
        return Sender().send_request(request_data, by_user=by_user)

    def patch_me(self, by_user: User, userName: str = None, password: str = None, email: str = None, firstName: str = None, middleName: str = None, lastName: str = None, phoneNumber: str = None, preferredLocale: str = None, isDismissed: bool = None, isDisabled: bool = None, position: str = None, extension: UserModelExtension = None, role: str = None, notification: UserModelNotification = None):
        """Partial update user
        :return: No Content
        """
        request_data = Build(url="/api/accounts/me").patch(userName=userName, password=password, email=email, firstName=firstName, middleName=middleName, lastName=lastName, phoneNumber=phoneNumber,
                                                           preferredLocale=preferredLocale, isDismissed=isDismissed, isDisabled=isDisabled, position=position, extension=extension, role=role, notification=notification,)
        return Sender().send_request(request_data, by_user=by_user)

    def change_password(self, by_user: User, oldPassword: str = None, newPassword: str = None):
        """Change password
        :return: No Content
        """
        request_data = Build(url="/api/accounts/change_password").put(
            oldPassword=oldPassword, newPassword=newPassword,)
        return Sender().send_request(request_data, by_user=by_user)

    def substitutionId(self, by_user: User):
        """Impersonate
        :return: Access token model
        """
        request_data = Build(
            url="/api/accounts/impersonate/{substitutionId}").post()
        return Sender().send_request(request_data, by_user=by_user)

    def unimpersonate(self, by_user: User):
        """Unimpersonate
        :return: Access token model
        """
        request_data = Build(url="/api/accounts/unimpersonate").post()
        return Sender().send_request(request_data, by_user=by_user)

    def debug_start(self, by_user: User):
        """Debug start
        :return: No Content
        """
        request_data = Build(url="/api/accounts/debug_start").post()
        return Sender().send_request(request_data, by_user=by_user)

    def debug_end(self, by_user: User):
        """Debug end
        :return: No Content
        """
        request_data = Build(url="/api/accounts/debug_end").post()
        return Sender().send_request(request_data, by_user=by_user)

    def substitutions(self, by_user: User):
        """Get account substitutions
        :return: User paging extended info
        """
        request_data = Build(url="/api/accounts/substitutions").get()
        return Sender().send_request(request_data, by_user=by_user)
