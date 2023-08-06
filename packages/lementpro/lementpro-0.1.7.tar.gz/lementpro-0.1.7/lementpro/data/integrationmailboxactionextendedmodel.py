#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class IntegrationMailboxActionExtendedModel:
    id: int = None
    integrationMailboxId: int = None
    objectTypeId: int = None
    rules: list = None
    autoReply: bool = None
    errorEmail: str = None
    executionInterval: int = None
