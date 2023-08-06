#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class ValueListExtendedModel:
    id: int = None
    companyId: int = None
    name: str = None
    description: str = None
    valueTypeId: str = None
    isSystem: bool = None
    values: list = None
