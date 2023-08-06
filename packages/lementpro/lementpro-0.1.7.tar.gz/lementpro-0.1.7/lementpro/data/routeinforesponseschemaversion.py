#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from lementpro.data.routeinforesponseschema import RouteInfoResponseSchema
@dataclass
class RouteInfoResponseSchemaVersion:
    id: int = None
    description: str = None
    dateCreated: str = None
    isActive: bool = None
    schema: RouteInfoResponseSchema = None
