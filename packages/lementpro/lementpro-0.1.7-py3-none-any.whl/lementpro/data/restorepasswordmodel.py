#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class RestorePasswordModel:
    login: str = None
    companyId: int = None
