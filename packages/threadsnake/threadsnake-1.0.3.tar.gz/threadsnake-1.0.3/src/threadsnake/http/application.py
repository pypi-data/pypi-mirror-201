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

from typing import Dict, List

from .core.httprequest import retrieve_query_pass
from .core.httpserver import HttpServer, HttpServerMessage
from .router import Router
from .types import Callback, Middleware
import __main__
import os

class Application(HttpServer, Router):
    def __init__(self, port: int, hostName: str = 'localhost', backlog: int = 8, chunkSize: int = 1024):
        HttpServer.__init__(self, port, hostName, backlog, chunkSize)
        Router.__init__(self)
        self.stack:List[Middleware] = []
        self.folder:str = os.path.dirname(__main__.__file__)
    
    def configure(self, middleware:Middleware):
        self.stack.append(middleware)
        return self

    def on_handle(self, message: HttpServerMessage) -> bytes:
        if len(message.data) == 0:
            return
        
        stack:List[Middleware] = self.stack.copy()
        
        def next():
            if len(stack) > 0 and not message.res.ended:
                stack.pop()(self, message.req, message.res, next)

        message.req = retrieve_query_pass(message.req)
        callback:Callback = None
        params:Dict[str, str]
        callback, params = self.test_path(message.req.method, message.req.path)
        if callback:
            message.req.params.update(params)
            stack.append(self.create_middleware(callback))

        stack.reverse()
        try:    
            next()
        except Exception as e:
            message.res.end(str(e)).status(500, 'Internal Server Error')

        return message.res.to_bytes()