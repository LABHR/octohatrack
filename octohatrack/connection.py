# Copyright (c) 2013 Alon Swartz <alon@turnkeylinux.org>
#
# This file is part of OctoHub.
#
# OctoHub is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 3 of the License, or (at your option) any later
# version.

import requests

from .response import parse_response

class Pager(object):
    def __init__(self, conn, uri, params, max_pages=0):
        """Iterator object handling pagination of Connection.send (method: GET)
            conn (octohub.Connection): Connection object
            uri (str): Request URI (e.g., /user/issues)
            params (dict): Parameters to include in request
            max_pages (int): Maximum amount of pages to get (0 for all)
        """
        self.conn = conn
        self.uri = uri
        self.params = params
        self.max_pages = max_pages
        self.per_page = 100
        self.count = 0

    def __iter__(self):
        while True:
            self.count += 1
            params = self.params.copy()
            params.setdefault('per_page', self.per_page)
            response = self.conn.send('GET', self.uri, params)
            yield response

            if self.count == self.max_pages:
                break

            if not 'next' in list(response.parsed_link.keys()):
                break

            self.uri = response.parsed_link.next.uri
            self.params = response.parsed_link.next.params

class Connection(object):
    def __init__(self, token=None):
        """OctoHub connection
            token (str): GitHub Token (anonymous if not provided)
        """
        self.endpoint = 'https://api.github.com'
        self.session = requests.Session()
        self.session.headers = {'User-Agent': 'octohub'}

        if token:
            self.session.headers['Authorization'] = 'token %s' % token

    def send(self, method, uri, params={}, data=None):
        """Prepare and send request
            method (str): Request HTTP method (e.g., GET, POST, DELETE, ...)
            uri (str): Request URI (e.g., /user/issues)
            params (dict): Parameters to include in request
            data (str | file type object): data to include in request

            returns: requests.Response object, including:
                response.parsed (AttrDict): parsed response when applicable
                response.parsed_link (AttrDict): parsed header link when applicable
                http://docs.python-requests.org/en/latest/api/#requests.Response
        """
        url = self.endpoint + uri
        kwargs = {'params': params, 'data': data}
        response = self.session.request(method, url, **kwargs)

        return parse_response(response)

