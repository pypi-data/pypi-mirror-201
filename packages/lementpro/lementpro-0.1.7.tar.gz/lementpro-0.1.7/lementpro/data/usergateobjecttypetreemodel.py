#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class UserGateObjectTypeTreeModel:
    id: int = None
    name: str = None
    isSystem: bool = None
    isAbstract: bool = None
    canCreateObject: bool = None
    children: list = None
