#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from lementpro.data.userinfoextensionmodel import UserInfoExtensionModel
from lementpro.data.userdetailedmodeldepartment import UserDetailedModelDepartment
from lementpro.data.userdetailedmodelnotification import UserDetailedModelNotification
from lementpro.data.actionlogentryinfomodel import ActionLogEntryInfoModel
@dataclass
class UserInfoExtendedModel:
    id: int = None
    userName: str = None
    companyId: int = None
    email: str = None
    firstName: str = None
    middleName: str = None
    lastName: str = None
    phoneNumber: str = None
    preferredLocale: str = None
    isDismissed: bool = None
    isDisabled: bool = None
    isSystem: bool = None
    position: str = None
    role: str = None
    departmentId: int = None
    displayName: str = None
    extension: UserInfoExtensionModel = None
    groupIds: list = None
    groups: list = None
    department: UserDetailedModelDepartment = None
    notification: UserDetailedModelNotification = None
    isDebug: bool = None
    entryInfo: ActionLogEntryInfoModel = None
