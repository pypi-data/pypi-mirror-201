#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from lementpro.data.mxgraphschemapoint import MxGraphSchemaPoint
@dataclass
class MxGraphSchemaElementModel:
    name: str = None
    description: str = None
    elementTypeId: str = None
    objectTypeId: int = None
    nameTemplate: str = None
    executors: list = None
    globalVariableName: str = None
    resolutionInSchema: bool = None
    subjectTemplate: str = None
    bodyTemplate: str = None
    properties: list = None
    id: str = None
    point: MxGraphSchemaPoint = None
