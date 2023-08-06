#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from lementpro.data.relatedobjectmodel import RelatedObjectModel
from lementpro.data.routeextendedresponseactivityelement import RouteExtendedResponseActivityElement
@dataclass
class UserGateRouteInstanceExtendedModelActivity:
    id: str = None
    dateCreated: str = None
    dateStarted: str = None
    dateCompleted: str = None
    statusId: str = None
    object: RelatedObjectModel = None
    variables: list = None
    element: RouteExtendedResponseActivityElement = None
