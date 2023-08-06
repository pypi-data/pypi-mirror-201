#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class ObjectTypeMenuPatchModel:
    name: str = None
    description: str = None
    url: str = None
    sortWeight: int = None
    iconClass: str = None
    isVisible: bool = None
