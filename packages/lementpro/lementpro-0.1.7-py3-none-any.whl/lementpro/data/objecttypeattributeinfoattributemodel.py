#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from lementpro.data.objecttypeattributeinfoattributerelationmodel import ObjectTypeAttributeInfoAttributeRelationModel
from lementpro.data.objecttypeattributeinfovaluelistmodel import ObjectTypeAttributeInfoValueListModel
@dataclass
class ObjectTypeAttributeInfoAttributeModel:
    knownId: str = None
    name: str = None
    description: str = None
    attributeTypeId: str = None
    valueTypeId: str = None
    relation: ObjectTypeAttributeInfoAttributeRelationModel = None
    valueList: ObjectTypeAttributeInfoValueListModel = None
    isSystem: bool = None
    isFilterable: bool = None
    isGroupable: bool = None
