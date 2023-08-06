#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from lementpro.data.departmentbossuserinfomodel import DepartmentBossUserInfoModel
from lementpro.data.actionlogentryinfomodel import ActionLogEntryInfoModel
@dataclass
class DepartmentInfoExtendedModel:
    id: int = None
    companyId: int = None
    parentId: int = None
    name: str = None
    description: str = None
    code: str = None
    sortWeight: int = None
    canHasSubDepartment: bool = None
    isHidden: bool = None
    isSystem: bool = None
    boss: DepartmentBossUserInfoModel = None
    dateCreated: str = None
    entryInfo: ActionLogEntryInfoModel = None
