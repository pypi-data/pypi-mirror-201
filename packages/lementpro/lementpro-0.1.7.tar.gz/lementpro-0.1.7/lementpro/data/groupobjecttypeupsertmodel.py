#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class GroupObjectTypeUpsertModel:
    objectTypeId: int = None
    rights: str = None
