#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class ValidationResponseItem:
    field: str = None
    message: str = None
