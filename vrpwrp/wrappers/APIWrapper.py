#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests

__author__ = 'Iván de Paz Centeno'


class APIWrapper(object):

    def __init__(self, API_URL):
        self.API_URL = API_URL

    def _request(self, method, params=None, data=None, is_binary=False):
        methods = {
            'GET': requests.get,
            'PUT': requests.put
        }

        if not is_binary and data is not None:
            data = data
            headers = {'content-type': 'application/json'}
        else:
            headers = {}

        response = methods[method](self.API_URL, params=params, data=data, headers=headers)
        return response.json()
