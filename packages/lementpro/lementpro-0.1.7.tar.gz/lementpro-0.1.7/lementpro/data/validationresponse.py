#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class ValidationResponse:
    message: str = None
    errors: list = None
