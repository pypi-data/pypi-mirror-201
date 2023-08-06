#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from lementpro.data.objecttypeattributeinfoattributemodel import ObjectTypeAttributeInfoAttributeModel
from lementpro.data.objecttypeattributeinfosettingsmodel import ObjectTypeAttributeInfoSettingsModel
from lementpro.data.objecttypeattributeinfoformulamodel import ObjectTypeAttributeInfoFormulaModel
@dataclass
class ObjectTypeAttributeExtendedModel:
    id: int = None
    objectTypeId: int = None
    attributeId: int = None
    attributeName: str = None
    attributeDescription: str = None
    attribute: ObjectTypeAttributeInfoAttributeModel = None
    settings: ObjectTypeAttributeInfoSettingsModel = None
    defaultValue: str = None
    valueFormat: str = None
    sortWeight: int = None
    isCalculated: bool = None
    isInherited: bool = None
    formula: ObjectTypeAttributeInfoFormulaModel = None
