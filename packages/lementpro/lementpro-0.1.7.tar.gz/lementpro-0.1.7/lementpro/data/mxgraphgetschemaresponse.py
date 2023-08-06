#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class MxGraphGetSchemaResponse:
    id: int = None
    name: str = None
    description: str = None
    elements: list = None
    transitions: list = None
    variables: list = None
