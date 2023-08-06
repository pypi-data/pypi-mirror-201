#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class UserFolderInfoModel:
    id: int = None
    parentId: int = None
    companyId: int = None
    name: str = None
    description: str = None
    menuObjectTypeId: int = None
    isSystem: bool = None
    isTemplate: bool = None
    isAbstract: bool = None
    sortWeight: int = None
    exportTemplateFileId: int = None
    isOwner: bool = None
