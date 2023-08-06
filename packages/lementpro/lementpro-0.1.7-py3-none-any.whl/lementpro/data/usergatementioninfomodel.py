#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from lementpro.data.usergatementioninfoobjectmodel import UserGateMentionInfoObjectModel
from lementpro.data.usergatementioninfocommentmodel import UserGateMentionInfoCommentModel
@dataclass
class UserGateMentionInfoModel:
    id: int = None
    userId: int = None
    object: UserGateMentionInfoObjectModel = None
    comment: UserGateMentionInfoCommentModel = None
