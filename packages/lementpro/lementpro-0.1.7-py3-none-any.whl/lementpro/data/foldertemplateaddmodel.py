#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from lementpro.data.folderaddobjectstatusfilter import FolderAddObjectStatusFilter
from lementpro.data.folderaddobjectstatefilter import FolderAddObjectStateFilter
from lementpro.data.folderaddobjectuserfilter import FolderAddObjectUserFilter
from lementpro.data.folderorderbyattributemodel import FolderOrderByAttributeModel
from lementpro.data.folderjoinbyattributemodel import FolderJoinByAttributeModel
@dataclass
class FolderTemplateAddModel:
    name: str = None
    description: str = None
    parentId: int = None
    menuObjectTypeId: int = None
    exportTemplateFileId: int = None
    isAbstract: bool = None
    objectTypes: list = None
    objectStatus: FolderAddObjectStatusFilter = None
    objectState: FolderAddObjectStateFilter = None
    objectUser: FolderAddObjectUserFilter = None
    orderByAttribute: FolderOrderByAttributeModel = None
    joinByAttribute: FolderJoinByAttributeModel = None
    groupByAttributes: list = None
    filterByAttributes: list = None
    userGroups: list = None
