#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class SchemaAddResponse:
    id: int = None
    versionId: int = None
    warnings: list = None
    errors: list = None
