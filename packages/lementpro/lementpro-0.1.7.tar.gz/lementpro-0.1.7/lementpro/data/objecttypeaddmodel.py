#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from lementpro.data.objecttypeaddextensionmodel import ObjectTypeAddExtensionModel
from lementpro.data.objecttypeaddcountermodel import ObjectTypeAddCounterModel
@dataclass
class ObjectTypeAddModel:
    knownId: str = None
    name: str = None
    description: str = None
    isAbstract: bool = None
    isDefault: bool = None
    isSealed: bool = None
    isChunk: bool = None
    parentId: int = None
    colorHex: str = None
    extension: ObjectTypeAddExtensionModel = None
    counter: ObjectTypeAddCounterModel = None
