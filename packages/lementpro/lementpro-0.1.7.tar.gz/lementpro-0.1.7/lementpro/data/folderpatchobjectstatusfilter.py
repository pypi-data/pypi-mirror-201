#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class FolderPatchObjectStatusFilter:
    open: bool = None
    closing: bool = None
    closed: bool = None
