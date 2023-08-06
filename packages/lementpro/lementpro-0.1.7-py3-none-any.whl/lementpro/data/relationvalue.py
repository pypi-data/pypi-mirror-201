#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class RelationValue:
    relatedTypeId: str = None
    multiplicity: int = None
    objectTypeId: int = None
    isAnySubTypeAvailable: bool = None
    values: list = None
