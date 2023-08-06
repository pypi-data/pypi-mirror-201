#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from lementpro.data.attributeaddrelationmodel import AttributeAddRelationModel
@dataclass
class AttributeAddModel:
    name: str = None
    description: str = None
    knownId: str = None
    units: str = None
    attributeTypeId: str = None
    valueTypeId: str = None
    isFilterable: bool = None
    isGroupable: bool = None
    valueListId: int = None
    relation: AttributeAddRelationModel = None
    precision: int = None
    widthInChars: int = None
    notifyAboutChanges: bool = None
