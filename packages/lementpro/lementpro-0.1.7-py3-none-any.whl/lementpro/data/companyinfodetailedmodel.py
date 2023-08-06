#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class CompanyInfoDetailedModel:
    usersTotalCount: int = None
    usersActiveCount: int = None
    dateAccessLast: str = None
