#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class GroupObjectExpirationPatchModel:
    expireSoon: int = None
    expire: int = None
