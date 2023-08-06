#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class FolderOrderByAttributeModel:
    attributeName: str = None
    attributeKnownId: str = None
    valueType: str = None
    order: str = None
