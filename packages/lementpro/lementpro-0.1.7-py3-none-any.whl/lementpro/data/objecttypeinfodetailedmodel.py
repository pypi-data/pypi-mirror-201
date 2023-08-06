#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from lementpro.data.objecttypeinfodetailedcountermodel import ObjectTypeInfoDetailedCounterModel
from lementpro.data.objecttypeinfodetailedmenumodel import ObjectTypeInfoDetailedMenuModel
from lementpro.data.objecttypeinfodetailedbimmodel import ObjectTypeInfoDetailedBimModel
@dataclass
class ObjectTypeInfoDetailedModel:
    counter: ObjectTypeInfoDetailedCounterModel = None
    exportTemplateFiles: list = None
    menu: ObjectTypeInfoDetailedMenuModel = None
    bim: ObjectTypeInfoDetailedBimModel = None
