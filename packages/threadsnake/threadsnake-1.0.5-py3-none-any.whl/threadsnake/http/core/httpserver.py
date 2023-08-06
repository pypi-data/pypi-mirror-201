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

import socket
from .httprequest import HttpRequest
from .httpresponse import HttpResponse
from .server import ClientAddress, Server

class HttpServerMessage:
    def __init__(self, client:socket.socket, address:ClientAddress, data:bytearray) -> None:
        self.client:socket.socket = client
        self.address:ClientAddress = address
        self.data:bytearray = None
        self.req:HttpRequest = None
        self.res:HttpResponse = HttpResponse()
        self.load_request(data)

    def load_request(self, data:bytearray):
        self.data = data
        try:
            self.req = HttpRequest(data.decode('latin-1'), self.client, self.address)
        except:
            self.res.status(403, 'Bad Request')
        return self

class HttpServer(Server):
    def __init__(self, port: int, hostName: str = 'localhost', backlog: int = 8, chunkSize: int = 1024) -> None:
        super().__init__(port, self.on_receive, hostName, backlog, chunkSize)

    def on_handle(self, message:HttpServerMessage) -> bytes:
        return b'HTTP/1.1 200 OK\n\n'

    def on_receive(self, client:socket.socket, address:ClientAddress, data:bytearray) -> bytes:
        if len(data) != 0:
            message = HttpServerMessage(client, address, data)
            return self.on_handle(message)
        return b'HTTP/1.1 200 OK\n\n'