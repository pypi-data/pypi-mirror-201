#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class UserGateObjectInfoChunkItemModel:
    id: int = None
    objectTypeId: int = None
    name: str = None
    parentId: int = None
    attributes: list = None
