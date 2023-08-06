#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class ObjectTypeAttributeInfoAttributeRelationModel:
    multiplicity: int = None
    relatedTypeId: str = None
    relationTypeId: str = None
    objectTypeId: int = None
    isAnySubTypeAvailable: bool = None
