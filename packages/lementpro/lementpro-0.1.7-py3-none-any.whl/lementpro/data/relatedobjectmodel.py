#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class RelatedObjectModel:
    id: int = None
    name: str = None
    isSystem: bool = None
    iconClass: str = None
    url: str = None
    userAvatarFileId: int = None
    userEmail: str = None
    userPhone: str = None
    fileSize: int = None
    fileDateCreated: str = None
    fileVersion: int = None
    fileUser: str = None
