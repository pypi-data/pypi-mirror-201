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

from time import time
from typing import Dict, Tuple
import uuid

from ...http.types import Middleware, Next
from ..core.session import Session
from ..core.httprequest import HttpRequest
from ..core.httpresponse import HttpResponse
from ..application import Application

def session(cookieName:str, durationSec:float = 300) -> Middleware:
    sessions:Dict[str, Tuple[Session, float]] = dict()
    lastCheck:float = time()

    def removeExpired():
        nonlocal lastCheck
        if time() - lastCheck > durationSec / 10:
            lastCheck = time()
            expiredSessions = [i for i in sessions if sessions[i][1] < time()]
            for e in expiredSessions:
                del sessions[e]

    def middleware(app:Application, req:HttpRequest, res:HttpResponse, next:Next):
        removeExpired()
        sessionId:str = None
        if cookieName not in req.cookies.values:
            sessionId = str(uuid.uuid4())
            res.set_cookie(cookieName, sessionId, durationSec)
        else:
            sessionId = req.cookies.values[cookieName]

        if sessionId not in sessions:
            sessions[sessionId] = [Session(), durationSec + time()]
        else:
            sessions[sessionId][1] = durationSec + time()

        req.session = sessions[sessionId][0]
        next()
    return middleware