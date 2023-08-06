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

from typing import Any, Dict

class Session:
    def __init__(self) -> None:
        self.values:Dict[str,Any] = dict()
    
    def set(self, key:str, value:Any):
        self.values[key] = value

    def has(self, key:str) -> bool:
        return key in self.values

    def get(self, key:str, default:Any) -> Any:
        if not self.has(key):
            self.set(key, default)
        return self.values[key]