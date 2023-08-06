#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class IntegrationMailboxActionPatchModel:
    objectTypeId: int = None
    rules: list = None
    autoReply: bool = None
    errorEmail: str = None
    executionInterval: int = None
