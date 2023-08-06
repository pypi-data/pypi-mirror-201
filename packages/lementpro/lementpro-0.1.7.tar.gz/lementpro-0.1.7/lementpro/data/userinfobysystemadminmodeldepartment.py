#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class UserInfoBySystemAdminModelDepartment:
    id: int = None
    name: str = None
    isBoss: bool = None
    isSystem: bool = None
