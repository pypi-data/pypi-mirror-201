#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from lementpro.data.folderaddobjectstatusfilter import FolderAddObjectStatusFilter
from lementpro.data.folderaddobjectstatefilter import FolderAddObjectStateFilter
from lementpro.data.folderaddobjectuserfilter import FolderAddObjectUserFilter
from lementpro.data.folderorderbyattributemodel import FolderOrderByAttributeModel
from lementpro.data.folderjoinbyattributemodel import FolderJoinByAttributeModel
@dataclass
class UserFolderExtendedModel:
    id: int = None
    parentId: int = None
    companyId: int = None
    name: str = None
    description: str = None
    menuObjectTypeId: int = None
    isSystem: bool = None
    isTemplate: bool = None
    isAbstract: bool = None
    sortWeight: int = None
    exportTemplateFileId: int = None
    objectStatus: FolderAddObjectStatusFilter = None
    objectState: FolderAddObjectStateFilter = None
    objectUser: FolderAddObjectUserFilter = None
    orderByAttribute: FolderOrderByAttributeModel = None
    joinByAttribute: FolderJoinByAttributeModel = None
    groupByAttributes: list = None
    filterByAttributes: list = None
    objectTypes: list = None
    viewTypeId: str = None
    countObjects: bool = None
    isOwner: bool = None
