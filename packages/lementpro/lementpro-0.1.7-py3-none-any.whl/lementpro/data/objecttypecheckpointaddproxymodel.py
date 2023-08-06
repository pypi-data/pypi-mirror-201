#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class ObjectTypeCheckpointAddProxyModel:
    name: str = None
    description: str = None
    delay: int = None
    duration: int = None
