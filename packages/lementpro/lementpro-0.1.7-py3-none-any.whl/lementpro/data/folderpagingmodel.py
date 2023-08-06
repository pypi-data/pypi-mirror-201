#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from lementpro.data.pagingmodel import PagingModel
@dataclass
class FolderPagingModel:
    paging: PagingModel = None
    total: int = None
    data: list = None
