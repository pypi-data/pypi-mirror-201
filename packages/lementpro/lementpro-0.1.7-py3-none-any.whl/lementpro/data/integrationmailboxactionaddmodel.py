#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class IntegrationMailboxActionAddModel:
    integrationMailboxId: int = None
    objectTypeId: int = None
    rules: list = None
    executionInterval: int = None
    autoReply: bool = None
    errorEmail: str = None
