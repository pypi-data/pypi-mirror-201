#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class ValueListAddModel:
    name: str = None
    description: str = None
    valueTypeId: str = None
    values: list = None
