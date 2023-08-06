#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class AccessTokenModel:
    accessToken: str = None
    refreshToken: str = None
    expiredIn: int = None
