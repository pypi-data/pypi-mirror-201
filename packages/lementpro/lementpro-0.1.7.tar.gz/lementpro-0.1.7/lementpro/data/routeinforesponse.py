#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from lementpro.data.routeinforesponseschemaversion import RouteInfoResponseSchemaVersion
@dataclass
class RouteInfoResponse:
    id: str = None
    companyId: int = None
    objectId: int = None
    dateCreated: str = None
    dateCompleted: str = None
    statusId: str = None
    debugSessionId: str = None
    schemaVersion: RouteInfoResponseSchemaVersion = None
