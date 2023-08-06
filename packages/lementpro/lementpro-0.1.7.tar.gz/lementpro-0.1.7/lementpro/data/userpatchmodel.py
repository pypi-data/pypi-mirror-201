#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from lementpro.data.usermodelextension import UserModelExtension
from lementpro.data.usermodelnotification import UserModelNotification
@dataclass
class UserPatchModel:
    userName: str = None
    password: str = None
    email: str = None
    firstName: str = None
    middleName: str = None
    lastName: str = None
    phoneNumber: str = None
    preferredLocale: str = None
    isDismissed: bool = None
    isDisabled: bool = None
    position: str = None
    extension: UserModelExtension = None
    role: str = None
    notification: UserModelNotification = None
