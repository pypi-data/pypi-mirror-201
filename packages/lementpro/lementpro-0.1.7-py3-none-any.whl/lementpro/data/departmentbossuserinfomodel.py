#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from lementpro.data.userinfoextensionmodel import UserInfoExtensionModel
@dataclass
class DepartmentBossUserInfoModel:
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
