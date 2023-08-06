#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class ObjectTypeInfoDetailedCounterModel:
    id: int = None
    useParentCounter: bool = None
    resetAfterNewYear: bool = None
    value: int = None
