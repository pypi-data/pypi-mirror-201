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

import os
from ...http.types import Middleware, Next
from ..core.httprequest import HttpRequest
from ..core.httpresponse import HttpResponse
from ..application import Application

def static(rootFolder:str = 'static') -> Middleware:
    def middleware(app:Application, req:HttpRequest, res:HttpResponse, next:Next):
        normalizedUrl = req.path.replace('\\', os.sep).replace('..', '')
        filename:str = os.sep.join([app.folder, rootFolder, normalizedUrl])
        if os.path.isfile(filename):
            res.read_file(filename)
        else:
            next()
    return middleware