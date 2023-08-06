#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class FolderGroupByAttributeModel:
    attributeName: str = None
    attributeKnownId: str = None
    valueType: str = None
