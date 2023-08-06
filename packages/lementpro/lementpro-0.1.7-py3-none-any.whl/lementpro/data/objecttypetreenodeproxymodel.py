#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class ObjectTypeTreeNodeProxyModel:
    id: int = None
    name: str = None
    isSystem: bool = None
    isAbstract: bool = None
    children: list = None
