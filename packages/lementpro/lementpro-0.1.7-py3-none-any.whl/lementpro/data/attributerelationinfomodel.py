#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class AttributeRelationInfoModel:
    multiplicity: int = None
    relationTypeId: str = None
    relatedTypeId: str = None
    notifyAboutExpiration: bool = None
    notifyAboutChanges: bool = None
    grantReadRights: bool = None
    grantEditRights: bool = None
    objectTypeKnownId: str = None
    objectTypeId: int = None
    inheritAccessRights: bool = None
    isNotSharable: bool = None
    isAnySubTypeAvailable: bool = None
    dependentAttributeId: int = None
    detachRelatedOnArchiving: bool = None
    detachRelatedOnDeleting: bool = None
    bimStateGroupId: int = None
