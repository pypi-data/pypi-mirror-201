#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class UserGateCategoryAddRequest:
    name: str = None
    knownId: str = None
    hasComments: bool = None
    menuIsVisible: bool = None
    menuUrl: str = None
    menuIconClass: str = None
    menuPosition: int = None
