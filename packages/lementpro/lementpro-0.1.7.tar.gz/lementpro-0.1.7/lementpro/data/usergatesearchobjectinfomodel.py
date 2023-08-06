#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class UserGateSearchObjectInfoModel:
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
    attributes: list = None
