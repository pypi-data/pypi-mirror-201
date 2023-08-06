from lementpro.builders import Build
from lementpro.data.user import User
from lementpro.sender import Sender


class Companies:
    """Service for working with Companies in UserGate Public API"""  
    def info(self, by_user: User):
        """Get company info by domain.
        :return: Company info
        """
        request_data = Build(url="/api/companies/info").get()
        return Sender().send_request(request_data, by_user=by_user)
        