#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class CompanyPasswordPolicyPatchModel:
    minLength: int = None
    upperCaseLength: int = None
    lowerCaseLength: int = None
    nonAlphaLength: int = None
    numericLength: int = None
