#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class UserDetailedModelNotification:
    id: int = None
    receiveNotificationByEmail: bool = None
    receiveNotificationOnNewObject: bool = None
    receiveNotificationOnChangedObject: bool = None
    receiveNotificationOnlyOnChangeInFavoriteObjects: bool = None
    receiveNotificationOnMentioned: bool = None
    receiveNotificationInVacation: bool = None
