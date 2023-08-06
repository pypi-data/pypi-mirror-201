#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from lementpro.data.objecttypeattributepatchsettingsmodel import ObjectTypeAttributePatchSettingsModel
from lementpro.data.objecttypeattributepatchformulamodel import ObjectTypeAttributePatchFormulaModel
@dataclass
class ObjectTypeAttributePatchModel:
    defaultValue: str = None
    valueFormat: str = None
    settings: ObjectTypeAttributePatchSettingsModel = None
    formula: ObjectTypeAttributePatchFormulaModel = None
