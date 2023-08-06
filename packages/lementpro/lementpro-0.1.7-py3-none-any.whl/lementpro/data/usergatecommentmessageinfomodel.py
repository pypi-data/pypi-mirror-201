#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from lementpro.data.commentextensionmodel import CommentExtensionModel
from lementpro.data.usergatecommentmessageinfousermodel import UserGateCommentMessageInfoUserModel
from lementpro.data.usergatecommentmessageinfousermodel import UserGateCommentMessageInfoUserModel
@dataclass
class UserGateCommentMessageInfoModel:
    id: int = None
    companyId: int = None
    objectId: int = None
    message: str = None
    parentId: int = None
    sourceId: str = None
    externalId: str = None
    extension: CommentExtensionModel = None
    dateCreated: str = None
    dateUpdated: str = None
    canEdit: bool = None
    dateViewed: str = None
    user: UserGateCommentMessageInfoUserModel = None
    userFrom: UserGateCommentMessageInfoUserModel = None
    files: list = None
