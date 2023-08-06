#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from lementpro.data.mxgraphschemaaddrequesttransitionconditionmodel import MxGraphSchemaAddRequestTransitionConditionModel
from lementpro.data.mxgraphschemapoint import MxGraphSchemaPoint
from lementpro.data.mxgraphschemaline import MxGraphSchemaLine
@dataclass
class MxGraphSchemaTransitionModel:
    name: str = None
    description: str = None
    sourceActions: list = None
    targetActions: list = None
    condition: MxGraphSchemaAddRequestTransitionConditionModel = None
    timer: int = None
    buttonTransition: bool = None
    buttonObjectAction: str = None
    id: str = None
    point: MxGraphSchemaPoint = None
    fromElementId: str = None
    toElementId: str = None
    line: MxGraphSchemaLine = None
