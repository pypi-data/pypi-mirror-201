#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from lementpro.data.attributepatchrelationmodel import AttributePatchRelationModel
@dataclass
class AttributePatchModel:
    name: str = None
    description: str = None
    units: str = None
    attributeTypeId: str = None
    valueTypeId: str = None
    isFilterable: bool = None
    isGroupable: bool = None
    valueListId: int = None
    relation: AttributePatchRelationModel = None
    precision: int = None
    widthInChars: int = None
    notifyAboutChanges: bool = None
