#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class FolderAttributePredicateModel:
    attributeName: str = None
    attributeKnownId: str = None
    valueType: str = None
    valueOperatorId: str = None
    value: str = None
