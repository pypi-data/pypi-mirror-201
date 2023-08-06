#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class RefreshTokenModel:
    refreshToken: str = None
