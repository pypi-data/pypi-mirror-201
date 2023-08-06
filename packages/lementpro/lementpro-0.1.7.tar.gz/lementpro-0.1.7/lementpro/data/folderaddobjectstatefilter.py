#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class FolderAddObjectStateFilter:
    expired: bool = None
    modified: bool = None
