#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class GroupInfoModel:
    id: int = None
    companyId: int = None
    name: str = None
    description: str = None
    dateCreated: str = None
    isSystem: bool = None
    uniqueId: str = None
    usersAmount: int = None
    avatarFileId: int = None
