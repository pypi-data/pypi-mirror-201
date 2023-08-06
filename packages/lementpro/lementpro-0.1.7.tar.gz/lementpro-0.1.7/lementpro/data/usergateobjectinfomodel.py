#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class UserGateObjectInfoModel:
    id: int = None
    objectTypeId: int = None
    name: str = None
    isDebug: bool = None
    canEdit: bool = None
    actions: str = None
    attributes: list = None
