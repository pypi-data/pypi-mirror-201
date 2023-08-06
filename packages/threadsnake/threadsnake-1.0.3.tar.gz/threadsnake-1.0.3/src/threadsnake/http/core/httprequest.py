##    Threadsnake. A tiny experimental server-side express-like library.
##    Copyright (C) 2022  Erick Fernando Mora Ramirez
##
##    This program is free software: you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation, either version 3 of the License, or
##    (at your option) any later version.
##
##    This program is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with this program.  If not, see <https://www.gnu.org/licenses/>.
##
##    mailto:erickfernandomoraramirez@gmail.com

import json
from socket import socket
from typing import Any, Dict, List

from .session import Session

from .common import decode_querystring, map_dictionary
from .constants import HEADER_CONTENT_TYPE, HEADER_COOKIES
from .server import ClientAddress

class HttpQuery:
    def __init__(self) -> None:
        self.url = ''
        self.querystring = ''
        self.path = ''
    
    def load_query(self, url:str) -> Dict[str, str]:
        self.url = url
        self.path = url
        if '?' in url:
            self.path, url = url.split('?', 1)
            self.querystring = decode_querystring(url)
            return map_dictionary(self.querystring, '&', '=')
        return dict()

class Cookies:
    def __init__(self, values:Dict[str, str] = None) -> None:
        self.values = values or dict()

    def load_cookies(self, raw:str):
        self.values = map_dictionary(raw, ';', '=')
        return self

class HttpRequest(HttpQuery):
    def __init__(self, raw:str, client:socket, clientAddress:ClientAddress) -> None:
        HttpQuery.__init__(self)
        self.client = client
        self.clientAddress = clientAddress
        self.headers:Dict[str, str] = {}
        self.params:Dict[str, str] = {}
        self.cookies:Cookies = Cookies()
        self.contentType:str = ''
        self.files:Dict[str, str] = {}
        self.authorization = {}
        self.session:Session = None
        self.data:Any = None
        self.raw = ''
        self.body:str = ''
        self.method:str = ''
        self.httpVersion:str = ''
        self.load(raw)

    def load(self, raw:str):
        self.raw = raw
        requestParts:List[str] = raw.split('\r\n\r\n', maxsplit=1)
        statusAndHeaders:List[str] = requestParts[0].split('\r\n')
        self.load_status(statusAndHeaders[0])
        self.load_headers(statusAndHeaders[1:])
        if len(requestParts) > 1:
            self.load_body(requestParts[1])

    def load_status(self, statusLine:str):
        status:List[str] = statusLine.split(' ')
        self.method = status[0]
        self.httpVersion = status[2] if len(status) > 2 else 'HTTP/1.1'
        if len(status) > 1:
            self.params = self.load_query(status[1])


    def load_headers(self, headers:List[str]):
        headerPairs:List[List[str]] = [
            [j.strip() for j in i.split(':', 1)] 
            for i in headers
            if len(i.split(':')) == 2
        ]
        self.headers = {header[0]:header[1] for header in headerPairs}
        if HEADER_COOKIES in self.headers:
            self.cookies = Cookies().load_cookies(self.headers[HEADER_COOKIES])
        if HEADER_CONTENT_TYPE in self.headers:
            self.contentType = self.headers[HEADER_CONTENT_TYPE]

    def load_body(self, body:str):
        self.body = body

    def json(self):
        try:
            return json.loads(self.body)
        except:
            return None

def retrieve_query_pass(req:HttpRequest) -> HttpRequest:
    if ':' in req.path:
        path:List[str] = req.path.split('/')
        req.path = '/'.join([i for i in path if len(i.split(':', 1)) != 2])
        req.params.update({i[0]:i[1] for i in path if len(i.split(':', 1)) == 2})
    return req