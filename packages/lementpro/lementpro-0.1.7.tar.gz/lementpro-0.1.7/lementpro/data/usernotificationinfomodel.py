#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class UserNotificationInfoModel:
    receiveNotificationByEmail: bool = None
    receiveNotificationOnNewObject: bool = None
    receiveNotificationOnChangedObject: bool = None
    receiveNotificationOnlyOnChangeInFavoriteObjects: bool = None
    receiveNotificationOnMentioned: bool = None
    receiveNotificationInVacation: bool = None
