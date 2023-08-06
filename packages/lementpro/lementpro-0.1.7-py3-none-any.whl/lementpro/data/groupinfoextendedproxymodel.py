#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from lementpro.data.actionlogentryinfomodel import ActionLogEntryInfoModel
from lementpro.data.groupobjectexpirationinfomodel import GroupObjectExpirationInfoModel
@dataclass
class GroupInfoExtendedProxyModel:
    id: int = None
    companyId: int = None
    name: str = None
    description: str = None
    dateCreated: str = None
    isSystem: bool = None
    uniqueId: str = None
    usersAmount: int = None
    avatarFileId: int = None
    entryInfo: ActionLogEntryInfoModel = None
    objectExpiration: GroupObjectExpirationInfoModel = None
