#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class ServiceIntegrationPatchModel:
    name: str = None
    description: str = None
    url: str = None
    contentTypeId: str = None
    methodId: str = None
