#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class GroupObjectExpirationInfoModel:
    id: int = None
    companyId: int = None
    groupId: int = None
    expireSoon: int = None
    expire: int = None
