#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from lementpro.data.objecttypeattributeaddsettingsmodel import ObjectTypeAttributeAddSettingsModel
from lementpro.data.objecttypeattributeaddformulamodel import ObjectTypeAttributeAddFormulaModel
@dataclass
class ObjectTypeAttributeAddProxyModel:
    attributeId: int = None
    defaultValue: str = None
    valueFormat: str = None
    settings: ObjectTypeAttributeAddSettingsModel = None
    formula: ObjectTypeAttributeAddFormulaModel = None
