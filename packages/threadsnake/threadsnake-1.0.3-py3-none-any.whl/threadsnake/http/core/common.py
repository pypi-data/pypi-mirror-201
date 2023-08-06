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

import re
import socket
import time
from typing import Any, Callable, Dict, List, Tuple

from .values.contenttypes import contentTypes
from .values.responsecodes import responseCodes

ClientAddress = Tuple[str, int]
OnReceiveCallback = Callable[[Any, socket.socket, ClientAddress], bytes]


def get_content_type(path:str):
    contentType = 'text/plain'
    if '.' in path:
        extension:str = path.split(".")[-1:][0]
        for i in contentTypes:
            if extension in contentTypes[i]:
                contentType = i
                if contentType.endswith("/"):
                    contentType += extension
                break
    return contentType

def map_dictionary(data:str, rowSeparator:str, keySeparator:str) -> Dict[str, str]:
    table:List[List[str]] = [
        [j.strip() for j in i.split(keySeparator, 1)]
        for i in data.split(rowSeparator) 
        if len(i.split(keySeparator)) == 2
    ]
    return {row[0]:row[1] for row in table}

def decode_querystring(data:str) -> Dict[str, str]:
    data = data.replace('+', ' ').replace('%20', ' ')#space
    data = data.replace('%2B', '+')#space
    data = data.replace('%7E', '~')#space
    references = [(i, chr(int(re.findall(r'[\d]+', i)[0]))) for i in re.findall(r'&#[\d]+;', data)]
    for ref in references:
        data = data.replace(ref[0], ref[1])
    return data

def get_cookie_expiration_UTC(durationSec:float) -> str:
    return time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime(time.time() + durationSec))

def get_port(port:int, max_port=65535) -> int:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while port <= max_port:
            try:
                sock.bind(('', port))
                sock.close()
                return port
            except OSError:
                port += 1
        else:
            raise IOError('no free ports')

def get_status_text_from_status_code(statusCode:int) -> str:
    return responseCodes.get(statusCode, 'Unknown')