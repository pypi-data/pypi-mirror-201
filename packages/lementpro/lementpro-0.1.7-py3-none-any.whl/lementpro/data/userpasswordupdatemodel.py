#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class UserPasswordUpdateModel:
    userId: int = None
    newPassword: str = None
