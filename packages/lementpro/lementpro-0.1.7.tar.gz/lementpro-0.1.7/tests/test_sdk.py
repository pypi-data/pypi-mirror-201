from lementpro.data.accesstokenmodel import AccessTokenModel
from lementpro.data.user import User
from lementpro.services.accounts import Accounts


def test_login():
    user = User(root_url="https://ugate.dev.lement.ru", specific_headers={"X-Lement-Host":"lementtest.dev.lement.ru"})
    resource = Accounts().login(login="dmoz", password="qwe", by_user=user).json()
    assert "accessToken" in resource


def test_get_me():
    user = User(root_url="https://ugate.dev.lement.ru", specific_headers={"X-Lement-Host": "lementtest.dev.lement.ru"})
    access_token = AccessTokenModel(**Accounts().login(login="dmoz", password="qwe", by_user=user).json()).accessToken
    user.access_token = access_token
    me = Accounts().get_me(by_user=user).json()
    assert me["entryInfo"]["dateUpdateLastUserDisplayName"] == "Дмитрий Мозжухин"