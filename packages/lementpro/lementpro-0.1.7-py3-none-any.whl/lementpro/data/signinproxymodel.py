#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class SignInProxyModel:
    login: str = None
    password: str = None
