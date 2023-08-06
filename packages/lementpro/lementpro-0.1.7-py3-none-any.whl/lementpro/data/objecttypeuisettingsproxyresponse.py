#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from lementpro.data.objecttypeuisettingsproxyresponsedetailedpage import ObjectTypeUiSettingsProxyResponseDetailedPage
from lementpro.data.objecttypeuisettingsproxyresponselistview import ObjectTypeUiSettingsProxyResponseListView
from lementpro.data.objecttypeuisettingsproxyresponsetableview import ObjectTypeUiSettingsProxyResponseTableView
from lementpro.data.objecttypeuisettingsproxyresponseeditpage import ObjectTypeUiSettingsProxyResponseEditPage
from lementpro.data.objecttypeuisettingsproxyresponsecreatepage import ObjectTypeUiSettingsProxyResponseCreatePage
@dataclass
class ObjectTypeUiSettingsProxyResponse:
    detailedPage: ObjectTypeUiSettingsProxyResponseDetailedPage = None
    listView: ObjectTypeUiSettingsProxyResponseListView = None
    tableView: ObjectTypeUiSettingsProxyResponseTableView = None
    editPage: ObjectTypeUiSettingsProxyResponseEditPage = None
    createPage: ObjectTypeUiSettingsProxyResponseCreatePage = None
