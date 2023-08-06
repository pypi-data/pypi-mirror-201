#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from lementpro.data.folderusertreecountmodel import FolderUserTreeCountModel
@dataclass
class UserFolderTreeNodeModel:
    id: int = None
    path: list = None
    parentId: int = None
    name: str = None
    isSystem: bool = None
    isTemplate: bool = None
    isAbstract: bool = None
    isVirtual: bool = None
    hasGrouping: bool = None
    isOwner: bool = None
    sortWeight: int = None
    countObjects: bool = None
    viewTypeId: str = None
    objectsCounter: FolderUserTreeCountModel = None
    children: list = None
