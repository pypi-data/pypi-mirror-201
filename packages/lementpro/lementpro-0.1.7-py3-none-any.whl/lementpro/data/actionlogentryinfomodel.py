#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class ActionLogEntryInfoModel:
    dateUpdateLast: str = None
    dateUpdateLastUserId: int = None
    dateUpdateLastUserDisplayName: str = None
    dateCreate: str = None
    dateCreateUserId: int = None
    dateCreateUserDisplayName: str = None
