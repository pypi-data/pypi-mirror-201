#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class UserGateSubstitutionModel:
    id: int = None
    userName: str = None
    email: str = None
    displayName: str = None
    avatarFileId: int = None
