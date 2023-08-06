#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class AttributeAddRelationModel:
    multiplicity: int = None
    relationTypeId: str = None
    relatedTypeId: str = None
    dependentAttributeId: int = None
    notifyAboutExpiration: bool = None
    notifyAboutChanges: bool = None
    grantReadRights: bool = None
    grantEditRights: bool = None
    objectTypeKnownId: str = None
    objectTypeId: int = None
    inheritAccessRights: bool = None
    isNotSharable: bool = None
    isAnySubTypeAvailable: bool = None
    bimStateGroupId: int = None
