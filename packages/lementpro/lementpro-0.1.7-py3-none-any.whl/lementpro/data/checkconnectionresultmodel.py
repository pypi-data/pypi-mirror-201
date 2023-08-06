#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class CheckConnectionResultModel:
    validImapSettings: bool = None
    validSmtpSettings: bool = None
