#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from lementpro.data.folderpatchobjectstatusfilter import FolderPatchObjectStatusFilter
from lementpro.data.folderpatchobjectstatefilter import FolderPatchObjectStateFilter
from lementpro.data.folderpatchobjectuserfilter import FolderPatchObjectUserFilter
from lementpro.data.folderorderbyattributemodel import FolderOrderByAttributeModel
from lementpro.data.folderjoinbyattributemodel import FolderJoinByAttributeModel
from lementpro.data.folderpatchreset import FolderPatchReset
@dataclass
class UserFolderPatchModel:
    name: str = None
    description: str = None
    objectTypes: list = None
    exportTemplateFileId: int = None
    objectStatus: FolderPatchObjectStatusFilter = None
    objectState: FolderPatchObjectStateFilter = None
    objectUser: FolderPatchObjectUserFilter = None
    orderByAttribute: FolderOrderByAttributeModel = None
    joinByAttribute: FolderJoinByAttributeModel = None
    groupByAttributes: list = None
    filterByAttributes: list = None
    isAbstract: bool = None
    reset: FolderPatchReset = None
    viewTypeId: str = None
    countObjects: bool = None
