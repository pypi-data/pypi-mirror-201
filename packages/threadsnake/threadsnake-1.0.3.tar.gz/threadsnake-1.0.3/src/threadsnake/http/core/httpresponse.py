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
from typing import Any, Dict, List
from .common import get_content_type, get_cookie_expiration_UTC, get_status_text_from_status_code
from .constants import HEADER_CONTENT_DISPOSITION, HEADER_CONTENT_LENGTH, HEADER_CONTENT_TYPE, HEADER_LOCATION, LINESEP

class ResponseHead:
    def __init__(self) -> None:
        self.httpVersion:str = 'HTTP/1.1'
        self.responseStatus:int = 404
        self.responseStatusText:str = 'NotFound'
        self.headers:Dict[str, List[str]] = dict()
    
    def append_header(self, name:str, value:str):
        if name not in self.headers:
            self.headers[name] = []
        self.headers[name].append(value)
    
    def set_header(self, name:str, value:str):
        self.headers[name] = [value]

    def get_header(self, name:str) -> str:
        if name in self.headers:
            return self.headers[name][0]
        return None
 
    def get_headers(self, name:str) -> List[str]:
        if name in self.headers:
            return self.headers[name]
        return None

    def remove_header(self, name:str) -> str:
        if name in self.headers:
            del self.headers[name]

    def set_cookie(self, name:str, value:str, durationSec:float = None, domain:str = None, path:str = None):
        cookieString = [value]
        if durationSec != None: cookieString.append(f'Expires={get_cookie_expiration_UTC(durationSec)}')
        if domain is not None: cookieString.append(f'Domain={domain}')
        if path is not None: cookieString.append(f'Path={path}')
        cookieHeader = f'{name}=' + '; '.join(cookieString)
        self.append_header('Set-Cookie', cookieHeader)

    def to_string(self) -> str:
        result:str = f'{self.httpVersion} {self.responseStatus} {self.responseStatusText} {LINESEP}'
        for header in self.headers:
            for headerValue in self.headers[header]:
                result += f'{header}: {headerValue}{LINESEP}'
        return result

class HttpResponse(ResponseHead):
    def __init__(self) -> None:
        ResponseHead.__init__(self)
        self.body:str = ''
        self.encoding:str = 'latin-1'
        self.ended:bool = False
    
    def end(self, data:str = None, status:int = None):
        self.ended = True
        return self.status(status).write(data)

    def status(self, responseCode:int = None, responseText:str = None):
        self.responseStatus = responseCode or self.responseStatus
        responseText = responseText or get_status_text_from_status_code(self.responseStatus)
        self.responseStatusText = responseText
        return self

    def append_header(self, name: str, value: str):
        ResponseHead.append_header(self, name, value)
        return self

    def set_header(self, name: str, value: str):
        ResponseHead.set_header(self, name, value)
        return self

    def set_cookie(self, name: str, value: str, durationSec: float = None, domain: str = None, path: str = None):
        ResponseHead.set_cookie(self, name, value, durationSec, domain, path)
        return self

    def content_disposition(self, value:str, fileName:str = None):
        if fileName is not None:
            value += f'; filename="{fileName}"'
        return self.set_header(HEADER_CONTENT_DISPOSITION, value)

    def content_type(self, value:str):
        return self.set_header(HEADER_CONTENT_TYPE, value)

    def redirect(self, value:str):
        return self.set_header(HEADER_LOCATION, value)

    def set_encoding(self, value:str):
        self.encoding = value
        return self

    def write(self, data:str):
        self.body += data
        return self

    def json(self, data:Any):
        return self\
        .write(json.dumps(data))\
        .content_type('application/json')\
        .status(200, 'OK')

    def html(self, data:str):
        return self\
        .write(data)\
        .content_type('text/html')\
        .status(200, 'OK')

    def read_file(self, fileName:str, encoding:str = None):
        self.set_encoding(encoding or self.encoding)
        with open(fileName, 'r', encoding=self.encoding) as f:
            self.write(f.read())
        return self.status(200, 'OK').content_type(get_content_type(fileName))

    def file(self, fileName:str, data:str, contentType:str = None, encoding:str = None):
        self.content_disposition('attachment', fileName)
        self.set_encoding(encoding or self.encoding)
        self.status(200, 'OK')
        if contentType is not None:
            self.content_type(contentType)
        self.body = data

    def download(self, path:str, fileName:str, contentType:str = None, encoding:str = None):
        self.fileName('attachment', fileName)
        self.body = ""
        return self.read_file(path, encoding)

    def to_bytes(self)->bytes:
        return str(self).encode(self.encoding)

    def __str__(self) -> str:
        if HEADER_LOCATION not in self.headers:
            self.set_header(HEADER_CONTENT_LENGTH, len(self.body))
        return ResponseHead.to_string(self) + LINESEP + self.body
