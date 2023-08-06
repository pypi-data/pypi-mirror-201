#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class UserGateObjectAddModel:
    name: str = None
    objectTypeId: int = None
    correctParentDates: bool = None
    bimElementIds: list = None
    objectAttributes: list = None
