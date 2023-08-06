#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class UserDetailedModelDepartment:
    id: int = None
    name: str = None
    isBoss: bool = None
    description: str = None
    isSystem: bool = None
