#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class FolderJoinByAttributeModel:
    attributeName: str = None
    attributeKnownId: str = None
    objectTypeId: int = None
