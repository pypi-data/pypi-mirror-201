#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from lementpro.data.usergatefolderobjectinfomodellastcommentuser import UserGateFolderObjectInfoModelLastCommentUser
from lementpro.data.usergatefolderobjectinfomodellastcommentuser import UserGateFolderObjectInfoModelLastCommentUser
@dataclass
class UserGateFolderObjectInfoModelLastComment:
    id: int = None
    user: UserGateFolderObjectInfoModelLastCommentUser = None
    userFrom: UserGateFolderObjectInfoModelLastCommentUser = None
    message: str = None
    messageSimplified: str = None
    dateCreated: str = None
    dateUpdated: str = None
    sourceId: str = None
