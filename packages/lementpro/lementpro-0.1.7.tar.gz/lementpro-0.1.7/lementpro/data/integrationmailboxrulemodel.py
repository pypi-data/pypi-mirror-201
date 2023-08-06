#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class IntegrationMailboxRuleModel:
    source: str = None
    targetKnownId: str = None
