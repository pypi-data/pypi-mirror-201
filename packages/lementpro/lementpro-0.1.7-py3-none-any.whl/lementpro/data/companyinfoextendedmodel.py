#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from lementpro.data.companycontactdetailsmodel import CompanyContactDetailsModel
from lementpro.data.companypasswordpolicymodel import CompanyPasswordPolicyModel
from lementpro.data.companylicensemodel import CompanyLicenseModel
from lementpro.data.companyextensionmodel import CompanyExtensionModel
from lementpro.data.actionlogentryinfomodel import ActionLogEntryInfoModel
from lementpro.data.companyinfodetailedmodel import CompanyInfoDetailedModel
@dataclass
class CompanyInfoExtendedModel:
    id: int = None
    name: str = None
    description: str = None
    maxUploadFileSize: int = None
    isReadOnly: bool = None
    isDisabled: bool = None
    timeZone: str = None
    isSchemaReadonly: bool = None
    contactDetails: CompanyContactDetailsModel = None
    passwordPolicy: CompanyPasswordPolicyModel = None
    license: CompanyLicenseModel = None
    dateCreated: str = None
    isSystem: bool = None
    extension: CompanyExtensionModel = None
    entryInfo: ActionLogEntryInfoModel = None
    detailed: CompanyInfoDetailedModel = None
