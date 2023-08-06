#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from lementpro.data.folderattributepredicatemodel import FolderAttributePredicateModel
@dataclass
class FolderFilterByAttributeModel:
    operator: str = None
    predicate: FolderAttributePredicateModel = None
    filters: list = None
