#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from lementpro.data.routeinforesponseschemaversion import RouteInfoResponseSchemaVersion
from lementpro.data.relatedobjectmodel import RelatedObjectModel
@dataclass
class UserGateRouteInstanceExtendedModel:
    id: str = None
    dateCreated: str = None
    dateCompleted: str = None
    statusId: str = None
    isDebug: bool = None
    schemaVersion: RouteInfoResponseSchemaVersion = None
    object: RelatedObjectModel = None
    activities: list = None
