from lementpro.builders import Build
from lementpro.data.user import User
from lementpro.sender import Sender


class Connections:
    """Service for working with Connections in UserGate Public API"""  
    def mailbox(self, by_user: User, login: str=None, password: str=None, smtpHost: str=None, smtpPort: int=None, imapHost: str=None, imapPort: int=None):
        """Check imap/smtp settings.
        :return: Mailbox integration info
        """
        request_data = Build(url="/api/connections/mailbox").post(login=login,password=password,smtpHost=smtpHost,smtpPort=smtpPort,imapHost=imapHost,imapPort=imapPort,)
        return Sender().send_request(request_data, by_user=by_user)
        