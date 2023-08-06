#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class MxGraphSchemaRelatedProperty:
    name: str = None
    description: str = None
    dataTypeId: str = None
    relatedTypeId: str = None
    defaultValue: str = None
    isRequired: bool = None
