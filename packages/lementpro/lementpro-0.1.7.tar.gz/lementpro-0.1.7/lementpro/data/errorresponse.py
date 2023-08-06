#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class ErrorResponse:
    code: int = None
    error: str = None
    message: str = None
