#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class FolderTemplatesTreeProxyModel:
    id: int = None
    parentId: int = None
    name: str = None
    description: str = None
    isSystem: bool = None
    isAbstract: bool = None
    sortWeight: int = None
    exportTemplateFileId: int = None
    children: list = None
