#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class UserViewInfoModel:
    id: int = None
    commentId: int = None
    userId: int = None
    dateCreated: str = None
