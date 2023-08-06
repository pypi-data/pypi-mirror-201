#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class ServiceIntegrationParamInfoPagingModel:
    id: int = None
    serviceIntegrationId: int = None
    paramTypeId: str = None
    key: str = None
    value: str = None
