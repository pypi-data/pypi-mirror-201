#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class UserGateAssistantModel:
    id: int = None
    assistantId: int = None
    userName: str = None
    email: str = None
    displayName: str = None
    avatarFileId: int = None
    isDisabled: bool = None
    isDismissed: bool = None
