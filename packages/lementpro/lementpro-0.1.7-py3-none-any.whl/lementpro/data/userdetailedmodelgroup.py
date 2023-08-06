#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class UserDetailedModelGroup:
    id: int = None
    name: str = None
    isSystem: bool = None
