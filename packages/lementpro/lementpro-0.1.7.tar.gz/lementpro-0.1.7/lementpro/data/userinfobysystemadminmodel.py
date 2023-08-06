#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from lementpro.data.userinfobysystemadminmodeldepartment import UserInfoBySystemAdminModelDepartment
from lementpro.data.userinfoextensionmodel import UserInfoExtensionModel
@dataclass
class UserInfoBySystemAdminModel:
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
    displayName: str = None
    avatarFileId: int = None
    department: UserInfoBySystemAdminModelDepartment = None
    groups: list = None
    extension: UserInfoExtensionModel = None
