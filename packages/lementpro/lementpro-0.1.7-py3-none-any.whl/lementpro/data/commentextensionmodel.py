#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from lementpro.data.commentemailextensionmodel import CommentEmailExtensionModel
from lementpro.data.commentemailextensionmodel import CommentEmailExtensionModel
@dataclass
class CommentExtensionModel:
    fromEmail: CommentEmailExtensionModel = None
    sendToEmail: CommentEmailExtensionModel = None
