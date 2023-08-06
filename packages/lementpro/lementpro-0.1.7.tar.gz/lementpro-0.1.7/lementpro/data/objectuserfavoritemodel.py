#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class ObjectUserFavoriteModel:
    objectIds: list = None
    isFavorite: bool = None
