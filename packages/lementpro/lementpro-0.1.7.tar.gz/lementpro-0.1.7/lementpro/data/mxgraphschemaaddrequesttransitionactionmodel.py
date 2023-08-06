#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class MxGraphSchemaAddRequestTransitionActionModel:
    sourceVariableTypeId: str = None
    sourceVariableName: str = None
    targetVariableTypeId: str = None
    targetVariableName: str = None
    constantValue: str = None
    order: int = None
