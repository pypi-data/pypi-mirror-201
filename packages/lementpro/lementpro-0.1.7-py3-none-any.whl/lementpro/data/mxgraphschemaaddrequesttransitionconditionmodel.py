#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from lementpro.data.mxgraphschemaaddrequesttransitionconditionpredicatemodel import MxGraphSchemaAddRequestTransitionConditionPredicateModel
@dataclass
class MxGraphSchemaAddRequestTransitionConditionModel:
    operator: str = None
    predicate: MxGraphSchemaAddRequestTransitionConditionPredicateModel = None
    conditions: list = None
