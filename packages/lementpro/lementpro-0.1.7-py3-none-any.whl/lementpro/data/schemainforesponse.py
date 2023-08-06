#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class SchemaInfoResponse:
    id: int = None
    name: str = None
    description: str = None
    isDeleted: bool = None
    objectTypeId: int = None
    versions: list = None
