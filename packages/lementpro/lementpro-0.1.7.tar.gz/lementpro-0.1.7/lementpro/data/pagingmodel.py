#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class PagingModel:
    current: int = None
    first: int = None
    last: int = None
    prev: int = None
    next: int = None
    total: int = None
