#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class IntegrationMailboxExtendedModel:
    id: int = None
    companyId: int = None
    name: str = None
    description: str = None
    login: str = None
    imapHost: str = None
    imapPort: int = None
    isDisabled: bool = None
