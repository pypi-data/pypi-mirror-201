#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class ObjectTypeAttributeAddSettingsModel:
    isRequired: bool = None
    isHidden: bool = None
    isSearchable: bool = None
    isImmutable: bool = None
    showOnCreate: bool = None
    showOnEdit: bool = None
    showInTable: bool = None
    showOnGeneralPage: bool = None
    showContentOnSeparatePage: bool = None
    showOnProjectPage: bool = None
    showNameInListView: bool = None
    showInListView: bool = None
    hideIfNull: bool = None
    wrapFieldOnNewRow: bool = None
    fillAvailableSpaceIfSingle: bool = None
    editorNullHint: str = None
