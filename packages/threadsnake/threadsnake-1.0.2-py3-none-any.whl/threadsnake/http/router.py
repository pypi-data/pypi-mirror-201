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
from typing import Any, Callable, Dict, List, Tuple

from .core.httprequest import HttpRequest
from .core.httpresponse import HttpResponse
from .types import Callback, CallbackMutator, Middleware, Next

class Router:

    patterns:List[Tuple[str, str]] = [
        (r"{([\w]+)\:int}", r"(?P<\1>[-]?[\\d]+)"), #Int pattern
        (r"{([\w]+)\:float}", r"(?P<\1>[-]?[\\d]+[\\.]?[\\d]?)"), #Float pattern
        (r"{([\w]+)\:re\(([\w\W]+?)\)}", r"(?P<\1>\2)"), #Regex pattern
        (r"{([\w]+)}", r"(?P<\1>[\\w]+)"), #General pattern
    ]

    def __init__(self) -> None:
        self.routes:Dict[str, Dict[str, Callback]] = dict()
        self.calbackMutator:CallbackMutator = lambda a: a

    def normalize_route(self, route:str) -> str:
        if not route.endswith('/'):
            route += '/'
        if not route.startswith('/'):
            route = '/' + route
        while '//' in route:
            route = route.replace('//', '/')  
        while route.endswith('/') and len(route) > 1:
            route = route[:-1]  
        return route
    
    def register_callback(self, httpMethod:str, route:str) -> CallbackMutator:
        ref:Router = self
        route = self.normalize_route(route)
        httpMethod = httpMethod.upper()
        def decorator(callback:Callback) -> Callback:
            callback = self.calbackMutator(callback)
            if httpMethod not in ref.routes:
                ref.routes[httpMethod] = {route:callback}
            else:
                ref.routes[httpMethod][route] = callback
            return callback
        return decorator

    def use_globally(self, mutator:CallbackMutator):
        currentMutator:CallbackMutator = self.calbackMutator
        newMutator:CallbackMutator = lambda c: mutator(currentMutator(c))
        self.calbackMutator = newMutator
        return self

    def get(self, route) -> CallbackMutator:
        return self.register_callback('GET', route)

    def post(self, route) -> CallbackMutator:
        return self.register_callback('POST', route)

    def put(self, route) -> CallbackMutator:
        return self.register_callback('PUT', route)

    def delete(self, route) -> CallbackMutator:
        return self.register_callback('DELETE', route)

    def use_router(self, router, root):
        for method in router.routes:
            for action in router.routes[method]:
                self.register_callback(method,f'{root}{action}')(router.routes[method][action])
        return self

    def serve(self, route:str, content:str, encoding:str):
        fileName:str = sub(sub(route, '/'), '\\')
        inner_callback:Callback = lambda app, req, res : res.file(fileName, content, encoding=encoding)
        self.get(route)(inner_callback)
        return self

    def __getattr__(self, method) -> Callable[[str],CallbackMutator]:
        def inner(route) -> CallbackMutator:
            return self.register_callback(method.upper(), route)
        return inner

    def test_path(self, method:str, path:str) -> Tuple[Callback, Dict[str,str]]:
        callback:Callback = None
        queryParams:Dict[str, str] = dict()
        if method.upper() in self.routes:
            paths:List[str] = self.routes[method.upper()].copy()
            for route in paths:
                pattern:str = route
                for regex in Router.patterns:
                    pattern = re.sub(regex[0], regex[1], pattern)
                match = re.match(f'^{pattern}$', path)
                if match:
                    callback = self.routes[method.upper()][route]
                    queryParams = match.groupdict()
                    break
        return callback, queryParams

    def create_middleware(self, callback:Callback) -> Middleware:
        def inner_callback(app:Any, req:HttpRequest, res:HttpResponse, next:Next):
            res.status(200, 'OK')
            callback(app, req, res)
            next()
        return inner_callback

def sub(data:str, token:str) -> str:
    return data if token not in data else data[data.index(token)+1:]

    