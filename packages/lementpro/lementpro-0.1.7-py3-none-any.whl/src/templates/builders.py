#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _io
from dataclasses import dataclass
from requests import Request


@dataclass
class Build:
    url: str

    def post(self, **kwargs):
        prop = self.get_url(**kwargs)
        return Request(method="post", url=self.url, json=prop)

    def put(self, **kwargs):
        prop = self.get_url(**kwargs)
        return Request(method="put", url=self.url, json=prop)

    def patch(self, **kwargs):
        prop = self.get_url(**kwargs)
        return Request(method="patch", url=self.url, json=prop)

    def post_with_file(self, file: _io.BufferedReader, form_field_name: str, **kwargs):
        file = {form_field_name: file}
        return Request(method="post", url=self.url, data=kwargs, files=file)

    def get(self, **kwargs):
        prop = self.get_url(**kwargs)
        return Request(method="get", url=self.url, json=prop)

    def delete(self, **kwargs):
        prop = self.get_url(**kwargs)
        return Request(method="delete", url=self.url, json=prop)

    def get_vars_from_path(self):
        vars_ = list()
        for part_way in self.url.split("/"):
            if "{" in part_way:
                vars_.append(part_way.replace("{", "").replace("}", ""))
        return vars_

    def get_url(self, **kwargs):
        var_in_path = self.get_vars_from_path()
        if var_in_path != list():
            self.url = self.url.format(**kwargs)
            for var in var_in_path:
                kwargs.pop(var)
        return kwargs
