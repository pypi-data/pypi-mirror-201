#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class ObjectTypeAttributeAddFormulaModel:
    formulaTypeId: str = None
    bimFunctionTypeId: str = None
    arguments: str = None
    formula: str = None
