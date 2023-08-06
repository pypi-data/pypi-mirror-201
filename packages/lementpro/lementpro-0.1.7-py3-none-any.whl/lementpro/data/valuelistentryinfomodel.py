#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class ValueListEntryInfoModel:
    valueListId: int = None
    id: int = None
    name: str = None
    value: str = None
