#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class CompanyInfoModel:
    companyId: int = None
    name: str = None
    isReadOnly: bool = None
    isDisabled: bool = None
    isSchemaReadonly: bool = None
    timeZone: str = None
    siteIconFile: int = None
    siteLogoFile: int = None
    siteName: str = None
