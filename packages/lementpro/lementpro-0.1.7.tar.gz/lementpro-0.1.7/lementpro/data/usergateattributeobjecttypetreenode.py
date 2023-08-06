#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class UserGateAttributeObjectTypeTreeNode:
    id: int = None
    name: str = None
    isSystem: bool = None
    isAbstract: bool = None
    hasAttribute: bool = None
    children: list = None
