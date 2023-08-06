#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class CompanyExtensionModel:
    siteIconFile: int = None
    siteLogoFile: int = None
    siteName: str = None
