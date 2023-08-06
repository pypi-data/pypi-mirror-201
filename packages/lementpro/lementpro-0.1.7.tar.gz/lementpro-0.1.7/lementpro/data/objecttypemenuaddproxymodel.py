#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class ObjectTypeMenuAddProxyModel:
    name: str = None
    description: str = None
    url: str = None
    isVisible: bool = None
    iconClass: str = None
