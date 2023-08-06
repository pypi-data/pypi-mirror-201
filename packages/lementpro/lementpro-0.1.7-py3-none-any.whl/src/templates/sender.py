#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from requests import Session
from .data.user import User
from .logger import logger


class Sender:

    @staticmethod
    def send_request(request_data, by_user=None):
        session = Sender().__set_user(by_user=by_user)
        request_data.url = by_user.root_url + request_data.url
        prepped = session.prepare_request(request_data)
        Sender.logging(prepped=prepped)
        response = session.send(request=prepped, timeout=30, verify=True)
        Sender.logging(prepped=response)
        return response

    @staticmethod
    def __set_user(by_user: User):
        session = Session()
        if by_user and by_user.access_token is not None:
            session.headers.update(Authorization=f'Bearer {by_user.access_token}')
        if by_user and by_user.specific_headers is not {}:
            session.headers.update(by_user.specific_headers)
        if by_user and by_user.cookies is not None:
            session.cookies = by_user.cookies
        return session

    @staticmethod
    def logging(prepped):
        if isinstance(prepped, requests.models.PreparedRequest):
            url, method, headers, body = prepped.url, prepped.method, prepped.headers, prepped.body
            info = f"sent request:\n url: {url}\n method: {method}\n headers: {headers}\n body: {body}\n "
        else:
            headers = prepped.headers
            info = f"received response:\n code: {prepped.status_code} {prepped.reason} \n headers: {headers} \n content: {prepped.text}"
        logger.debug("len logging =%s" % str(len(info)))
        if len(info) < 10000:
            logger.debug(f'\n\n{info}')
        else:
            logger.debug("Log is too large.")
            logger.debug("Return only header = %s" % headers)
