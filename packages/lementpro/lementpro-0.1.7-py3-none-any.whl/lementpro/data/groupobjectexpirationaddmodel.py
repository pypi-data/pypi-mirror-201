#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class GroupObjectExpirationAddModel:
    groupId: int = None
    expireSoon: int = None
    expire: int = None
