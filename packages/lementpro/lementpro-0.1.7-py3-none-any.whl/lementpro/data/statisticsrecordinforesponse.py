#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class StatisticsRecordInfoResponse:
    schemaId: int = None
    elementTypeId: str = None
    duration: str = None
    schemaVersionId: int = None
    routeInstanceId: str = None
    executorId: int = None
    objectId: int = None
    elementName: str = None
    dateCreated: str = None
    dateStarted: str = None
    dateCompleted: str = None
