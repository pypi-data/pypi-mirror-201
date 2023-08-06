#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class MxGraphSchemaLine:
    points: list = None
    css: str = None
    elbow: str = None
    edgeStyle: str = None
