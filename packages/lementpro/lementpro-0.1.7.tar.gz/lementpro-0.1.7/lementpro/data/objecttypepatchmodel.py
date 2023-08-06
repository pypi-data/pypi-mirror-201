#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from lementpro.data.objecttypepatchextensionmodel import ObjectTypePatchExtensionModel
from lementpro.data.objecttypepatchcountermodel import ObjectTypePatchCounterModel
@dataclass
class ObjectTypePatchModel:
    knownId: str = None
    name: str = None
    description: str = None
    isAbstract: bool = None
    isDefault: bool = None
    isSealed: bool = None
    isChunk: bool = None
    colorHex: str = None
    extension: ObjectTypePatchExtensionModel = None
    counter: ObjectTypePatchCounterModel = None
    sortWeight: int = None
