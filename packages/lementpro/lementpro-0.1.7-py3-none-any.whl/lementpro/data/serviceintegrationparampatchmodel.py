#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class ServiceIntegrationParamPatchModel:
    paramTypeId: str = None
    key: str = None
    value: str = None
