#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class UserMailboxExtendedModel:
    id: int = None
    companyId: int = None
    userId: int = None
    login: str = None
    smtpHost: str = None
    smtpPort: int = None
    imapHost: str = None
    imapPort: int = None
    isDisabled: bool = None
    signature: str = None
    passwordHash: str = None
