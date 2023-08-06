#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class ObjectTypeInfoDetailedMenuModel:
    id: int = None
    name: str = None
    description: str = None
    url: str = None
    sortWeight: int = None
    iconClass: str = None
    isVisible: bool = None
    iconFileId: int = None
    isSystem: bool = None
