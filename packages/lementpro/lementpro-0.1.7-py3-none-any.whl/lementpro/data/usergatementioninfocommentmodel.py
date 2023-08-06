#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from lementpro.data.usergatecommentmessageinfousermodel import UserGateCommentMessageInfoUserModel
@dataclass
class UserGateMentionInfoCommentModel:
    id: int = None
    message: str = None
    dateCreated: str = None
    user: UserGateCommentMessageInfoUserModel = None
