#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class ChangePasswordModel:
    oldPassword: str = None
    newPassword: str = None
