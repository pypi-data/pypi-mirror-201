#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class RouteInfoResponseSchema:
    id: int = None
    name: str = None
    description: str = None
    dateCreated: str = None
    isDeleted: bool = None
