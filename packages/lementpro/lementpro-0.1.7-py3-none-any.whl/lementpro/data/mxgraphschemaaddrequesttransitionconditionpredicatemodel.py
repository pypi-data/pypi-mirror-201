#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class MxGraphSchemaAddRequestTransitionConditionPredicateModel:
    propertyName: str = None
    globalVariableName: str = None
    valueTypeId: str = None
    conditionValueOperatorId: str = None
    value: str = None
