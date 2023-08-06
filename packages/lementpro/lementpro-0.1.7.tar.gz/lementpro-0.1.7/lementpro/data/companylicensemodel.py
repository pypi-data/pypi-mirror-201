#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class CompanyLicenseModel:
    maxEmployeeCount: int = None
    dateExpired: str = None
    features: list = None
