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

from ..core.httpresponse import HttpResponse

def status(res:HttpResponse, responseCode:int) -> None:
    res.status(responseCode)

def not_found(res:HttpResponse) -> None:
    res.status(404, "NotFound")

def bad_request(res:HttpResponse) -> None:
    res.status(400, "BadRequest")

def ok(res:HttpResponse) -> None:
    res.status(200, "Ok")