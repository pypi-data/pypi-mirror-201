#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from lementpro.data.groupobjectexpirationpatchmodel import GroupObjectExpirationPatchModel
@dataclass
class GroupUpdateProxyModel:
    name: str = None
    description: str = None
    avatarFileId: int = None
    objectExpiration: GroupObjectExpirationPatchModel = None
