#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class FolderPatchReset:
    exportTemplateFileId: bool = None
    orderByAttribute: bool = None
    filterByAttributes: bool = None
    groupByAttributes: bool = None
    joinByAttribute: bool = None
