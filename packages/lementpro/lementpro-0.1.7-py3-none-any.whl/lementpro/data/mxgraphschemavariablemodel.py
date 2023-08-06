#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class MxGraphSchemaVariableModel:
    name: str = None
    description: str = None
    dataTypeId: str = None
    relatedTypeId: str = None
    bindElementProperty: str = None
    isRouteObject: bool = None
    relatedProperties: list = None
