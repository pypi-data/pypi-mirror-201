#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from lementpro.data.emailaddressmodel import EmailAddressModel
@dataclass
class CommentAddByUserModel:
    objectId: int = None
    objectName: str = None
    message: str = None
    parentId: int = None
    emailAddress: EmailAddressModel = None
    mentionedUserIds: list = None
    fileIds: list = None
