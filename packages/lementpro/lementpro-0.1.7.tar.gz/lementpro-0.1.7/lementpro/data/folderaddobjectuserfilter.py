#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class FolderAddObjectUserFilter:
    isMember: bool = None
    isController: bool = None
    isFavorite: bool = None
    canRead: bool = None
    canEdit: bool = None
    canDelete: bool = None
