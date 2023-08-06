#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class ObjectTypeBreadCrumbModel:
    name: str = None
    isSystem: bool = None
