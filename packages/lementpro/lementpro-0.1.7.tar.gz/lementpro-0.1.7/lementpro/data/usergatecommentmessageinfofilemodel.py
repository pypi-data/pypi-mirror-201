#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class UserGateCommentMessageInfoFileModel:
    id: int = None
    dateCreated: str = None
    fileName: str = None
    fileSize: int = None
