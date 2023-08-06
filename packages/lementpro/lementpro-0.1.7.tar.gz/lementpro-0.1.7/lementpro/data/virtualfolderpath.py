#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class VirtualFolderPath:
    knownId: str = None
    value: str = None
