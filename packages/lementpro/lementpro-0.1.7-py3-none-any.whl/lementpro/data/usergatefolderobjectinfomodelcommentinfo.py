#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from lementpro.data.usergatefolderobjectinfomodellastcomment import UserGateFolderObjectInfoModelLastComment
@dataclass
class UserGateFolderObjectInfoModelCommentInfo:
    total: int = None
    numUnread: int = None
    lastComment: UserGateFolderObjectInfoModelLastComment = None
