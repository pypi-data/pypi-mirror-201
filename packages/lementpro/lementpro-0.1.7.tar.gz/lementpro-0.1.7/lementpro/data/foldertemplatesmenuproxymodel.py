#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class FolderTemplatesMenuProxyModel:
    id: int = None
    name: str = None
    description: str = None
    objectTypeId: int = None
    url: str = None
    sortWeight: int = None
    iconClass: str = None
    isVisible: bool = None
    iconFileId: int = None
    isSystem: bool = None
    folders: list = None
