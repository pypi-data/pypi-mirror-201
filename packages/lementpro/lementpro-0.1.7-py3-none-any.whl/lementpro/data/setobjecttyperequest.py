#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class SetObjectTypeRequest:
    objectTypeId: int = None
    needStartAfterCreateObject: bool = None
