#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from lementpro.data.routeextendedresponsereferenceobject import RouteExtendedResponseReferenceObject
@dataclass
class RouteExtendedResponseActivityVariable:
    name: str = None
    variableTypeId: str = None
    dataTypeId: str = None
    relatedTypeId: str = None
    value: str = None
    reference: RouteExtendedResponseReferenceObject = None
    referenceArray: list = None
    isRequired: bool = None
