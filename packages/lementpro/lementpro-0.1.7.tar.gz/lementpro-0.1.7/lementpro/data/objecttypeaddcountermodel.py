#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class ObjectTypeAddCounterModel:
    useParentCounter: bool = None
    resetAfterNewYear: bool = None
    value: int = None
