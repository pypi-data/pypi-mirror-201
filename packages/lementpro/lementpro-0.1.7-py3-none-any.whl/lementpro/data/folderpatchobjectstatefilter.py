#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class FolderPatchObjectStateFilter:
    expired: bool = None
    modified: bool = None
