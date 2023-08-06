#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class ObjectTypeBimPatchModel:
    icon: str = None
    hint: str = None
    showCreateBtn: bool = None
    calcElementState: bool = None
