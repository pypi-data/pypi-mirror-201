#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass


@dataclass
class User:
    root_url: str
    login: str = None
    password: str = None
    access_token: str = None
    cookies: str = None
    specific_headers: dict = None
