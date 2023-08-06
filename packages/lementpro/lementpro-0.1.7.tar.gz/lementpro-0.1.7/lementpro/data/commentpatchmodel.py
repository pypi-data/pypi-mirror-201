#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from lementpro.data.emailaddressmodel import EmailAddressModel
@dataclass
class CommentPatchModel:
    message: str = None
    emailAddress: EmailAddressModel = None
    mentionedUserIds: list = None
    fileIds: list = None
