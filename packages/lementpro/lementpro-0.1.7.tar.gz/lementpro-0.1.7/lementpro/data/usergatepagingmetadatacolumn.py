#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class UserGatePagingMetadataColumn:
    name: str = None
    key: str = None
    isSystem: bool = None
    isSortable: bool = None
