#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from lementpro.data.objecttypeattributeinfovaluelistmodel import ObjectTypeAttributeInfoValueListModel
from lementpro.data.relationvalue import RelationValue
@dataclass
class UserGateSearchObjectInfoAttributeModel:
    id: int = None
    knownId: str = None
    name: str = None
    isSystem: bool = None
    value: str = None
    valueList: ObjectTypeAttributeInfoValueListModel = None
    relationValue: RelationValue = None
    attributeTypeId: str = None
    valueTypeId: str = None
    relationTypeId: str = None
    isRequired: bool = None
    isEditable: bool = None
