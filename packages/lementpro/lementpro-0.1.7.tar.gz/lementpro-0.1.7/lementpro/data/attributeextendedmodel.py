#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from lementpro.data.attributerelationinfomodel import AttributeRelationInfoModel
@dataclass
class AttributeExtendedModel:
    id: int = None
    knownId: str = None
    name: str = None
    description: str = None
    units: str = None
    attributeTypeId: str = None
    valueTypeId: str = None
    valueListId: int = None
    isFilterable: bool = None
    isGroupable: bool = None
    isInternal: bool = None
    precision: int = None
    widthInChars: int = None
    notifyAboutChanges: bool = None
    nullValueHint: str = None
    relation: AttributeRelationInfoModel = None
