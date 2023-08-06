#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class UserInfoExtensionModel:
    avatarFileId: int = None
    additional: str = None
    systemTheme: str = None
    startupPage: str = None
    showSystemFoldersObjectsCount: bool = None
