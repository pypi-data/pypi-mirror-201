#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from lementpro.data.companycontactdetailspatchmodel import CompanyContactDetailsPatchModel
from lementpro.data.companypasswordpolicypatchmodel import CompanyPasswordPolicyPatchModel
from lementpro.data.companyextensionmodel import CompanyExtensionModel
@dataclass
class CompanyPatchModel:
    name: str = None
    description: str = None
    maxUploadFileSize: int = None
    isReadOnly: bool = None
    isDisabled: bool = None
    isSchemaReadonly: bool = None
    timeZone: str = None
    contactDetails: CompanyContactDetailsPatchModel = None
    passwordPolicy: CompanyPasswordPolicyPatchModel = None
    extension: CompanyExtensionModel = None
