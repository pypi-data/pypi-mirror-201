#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class FileUploadResultModel:
    fileId: int = None
    name: str = None
    bytes: int = None
    dateCreated: str = None
    dateDeleted: str = None
    isFullyUploadedToStorage: bool = None
    fileGroupId: int = None
    numberInGroup: int = None
    isLastInGroup: bool = None
    isFinal: bool = None
    userId: int = None
    userIdFrom: int = None
