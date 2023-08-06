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

from base64 import b64decode
from ...http.types import Next
from ..core.httprequest import HttpRequest
from ..core.httpresponse import HttpResponse
from ..application import Application

def authorization(app:Application, req:HttpRequest, res:HttpResponse, next:Next) -> None:
    authKey:str = 'Authorization'
    if authKey in req.headers:
        authType, authValue = req.headers[authKey].split(' ', 1)
        req.authorization[authType] = ''
        if authType == 'Bearer':
            req.authorization[authType] = authValue 
        elif authType == 'Basic':
            user, password = b64decode(authValue.encode()).decode().split(':')
            req.authorization[authType] = {'user':user, 'password':password}
        del req.headers[authKey]
    next()