#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from lementpro.data.departmentinfomodel import DepartmentInfoModel
@dataclass
class DepartmentTreeModel:
    id: int = None
    general: DepartmentInfoModel = None
    children: list = None
