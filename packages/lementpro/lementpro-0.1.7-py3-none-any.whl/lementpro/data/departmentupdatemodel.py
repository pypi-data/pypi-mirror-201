#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class DepartmentUpdateModel:
    parentId: int = None
    name: str = None
    description: str = None
    code: str = None
    sortWeight: int = None
    isHidden: bool = None
    bossUserId: int = None
