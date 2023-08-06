#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class ObjectTypeCheckpointInfoExtendedModel:
    id: int = None
    name: str = None
    description: str = None
    objectTypeId: int = None
    delay: int = None
    duration: int = None
