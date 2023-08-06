#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class ObjectTypeAttributeInfoFormulaModel:
    formulaTypeId: str = None
    bimFunctionTypeId: str = None
    formula: str = None
    arguments: str = None
