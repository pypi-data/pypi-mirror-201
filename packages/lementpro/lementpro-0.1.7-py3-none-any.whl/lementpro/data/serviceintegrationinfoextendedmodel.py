#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from lementpro.data.serviceintegrationinfodetailedmodel import ServiceIntegrationInfoDetailedModel
@dataclass
class ServiceIntegrationInfoExtendedModel:
    id: int = None
    companyId: int = None
    name: str = None
    description: str = None
    url: str = None
    contentTypeId: str = None
    methodId: str = None
    detailed: ServiceIntegrationInfoDetailedModel = None
