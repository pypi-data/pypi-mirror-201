#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class GroupAddModel:
    name: str = None
    description: str = None
    avatarFileId: int = None
