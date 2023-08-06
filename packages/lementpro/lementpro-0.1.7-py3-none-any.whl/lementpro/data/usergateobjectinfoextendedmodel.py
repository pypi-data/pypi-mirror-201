#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from lementpro.data.usergateobjectinfoextendedmodelroutedata import UserGateObjectInfoExtendedModelRouteData
@dataclass
class UserGateObjectInfoExtendedModel:
    id: int = None
    objectTypeId: int = None
    name: str = None
    dateCreated: str = None
    dateExpire: str = None
    dateModified: str = None
    dateArchived: str = None
    isClosing: bool = None
    isFavorite: bool = None
    isModified: bool = None
    isDebug: bool = None
    actions: str = None
    attributes: list = None
    route: UserGateObjectInfoExtendedModelRouteData = None
    canEdit: bool = None
