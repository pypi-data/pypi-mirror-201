#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from lementpro.data.usergateobjectaddmodel import UserGateObjectAddModel
@dataclass
class UserGateExecuteObjectActionModel:
    dateEnd: str = None
    userIds: list = None
    comment: str = None
    relatedObjectIds: list = None
    relationAttributeKnownId: str = None
    newObject: UserGateObjectAddModel = None
