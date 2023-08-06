#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class IntegrationMailboxAddModel:
    name: str = None
    description: str = None
    login: str = None
    password: str = None
    imapHost: str = None
    imapPort: int = None
    isDisabled: bool = None
