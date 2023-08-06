#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class GroupObjectTypeInfoModel:
    id: int = None
    companyId: int = None
    objectTypeId: int = None
    groupId: int = None
    rights: str = None
