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

import asyncio
import socket
from .common import ClientAddress, OnReceiveCallback

class Server:
    def __init__(self, port:int, onReceive:OnReceiveCallback, hostName:str = 'localhost', backlog:int = 8, chunkSize:int = 1024) -> None:
        self.port = port
        self.hostname = hostName
        self.backlog = backlog
        self.chunkSize = chunkSize
        self.onReceive = onReceive

    def loop(self):
        return asyncio.get_event_loop()

    async def read(self, client:socket.socket, size:int) -> bytes:
        try:
            return await asyncio.wait_for(self.loop().sock_recv(client, size), 0.1)
        except Exception as e:
            return b''

    async def on_accept(self, client:socket.socket, address:ClientAddress):
        data:bytearray = bytearray()
        while True:
            chunk:bytes = await self.read(client, self.chunkSize)
            if len(chunk) == 0:
                break
            data.extend(chunk)
        response:bytes = self.onReceive(client, address, data)
        await self.loop().sock_sendall(client, response)
        client.close()

    async def run(self):
        serverSocket:socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.bind((self.hostname, self.port))
        serverSocket.listen(self.backlog)
        serverSocket.setblocking(False)
        
        loop:asyncio.AbstractEventLoop = self.loop()

        while True:
            client:socket.socket = None
            address:ClientAddress = ('', 0)
            client, address = await loop.sock_accept(serverSocket)
            loop.create_task(self.on_accept(client, address))

    def start(self):
        asyncio.run(self.run())