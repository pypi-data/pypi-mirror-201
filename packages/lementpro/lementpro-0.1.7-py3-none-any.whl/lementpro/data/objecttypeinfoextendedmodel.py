#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from lementpro.data.objecttypeextensionmodel import ObjectTypeExtensionModel
from lementpro.data.objecttypeinfodetailedmodel import ObjectTypeInfoDetailedModel
@dataclass
class ObjectTypeInfoExtendedModel:
    id: int = None
    companyId: int = None
    knownId: str = None
    name: str = None
    description: str = None
    isAbstract: bool = None
    isDefault: bool = None
    isSealed: bool = None
    isChunk: bool = None
    parentId: int = None
    isSystem: bool = None
    sortWeight: int = None
    colorHex: str = None
    extension: ObjectTypeExtensionModel = None
    systemObjectTypeId: str = None
    detailed: ObjectTypeInfoDetailedModel = None
