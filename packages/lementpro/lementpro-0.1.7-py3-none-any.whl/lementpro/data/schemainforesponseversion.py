#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class SchemaInfoResponseVersion:
    id: int = None
    description: str = None
    dateCreated: str = None
    isDraft: bool = None
    isActive: bool = None
