#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class CompanyContactDetailsModel:
    phone: str = None
    email: str = None
    name: str = None
    skype: str = None
    locale: str = None
