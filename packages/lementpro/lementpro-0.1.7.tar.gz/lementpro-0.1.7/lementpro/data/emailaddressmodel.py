#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from lementpro.data.toemailsmodel import ToEmailsModel
from lementpro.data.toccmodel import ToCcModel
from lementpro.data.tobccmodel import ToBccModel
@dataclass
class EmailAddressModel:
    toEmails: ToEmailsModel = None
    toCc: ToCcModel = None
    toBcc: ToBccModel = None
